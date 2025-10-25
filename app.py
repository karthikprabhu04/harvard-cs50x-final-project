from flask import Flask, render_template, request, jsonify
import os
import subprocess
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process_audio():
    # Save uploaded audio
    file = request.files["audio"]
    filepath = os.path.abspath(os.path.join(UPLOAD_FOLDER, "lecture.wav"))
    file.save(filepath)

    # Define paths
    whisper_exe = os.path.join("whisper.cpp", "build", "bin", "Release", "whisper-cli.exe")
    model_path = os.path.abspath(os.path.join("whisper.cpp", "models", "ggml-base.en.bin"))
    transcript_path = os.path.join(UPLOAD_FOLDER, "lecture.wav.txt")

    # Run Whisper.cpp command (transcribe audio)
    subprocess.run([
        whisper_exe,
        "-m", model_path,
        "-f", filepath,
        "-otxt"
    ], cwd=os.path.dirname(whisper_exe))

    # Ensure transcript file exists
    if not os.path.exists(transcript_path):
        # Sometimes Whisper saves the output next to the .exe
        fallback_path = os.path.join(os.path.dirname(whisper_exe), "lecture.wav.txt")
        if os.path.exists(fallback_path):
            os.rename(fallback_path, transcript_path)
        else:
            return jsonify({"error": "Transcription failed, no output file found"}), 500

    # Read transcript
    with open(transcript_path, "r", encoding="utf-8") as f:
        transcript = f.read().strip()

    # Summarise transcript (using Sumy)
    parser = PlaintextParser.from_string(transcript, Tokenizer("english"))
    summarizer = LexRankSummarizer()
    summary_sentences = summarizer(parser.document, 3)
    summary = " ".join(str(s) for s in summary_sentences)

    return jsonify({"transcript": transcript, "summary": summary})


if __name__ == "__main__":
    app.run(debug=True)