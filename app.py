from flask import Flask, render_template, request, jsonify
import os, subprocess
from transformers import pipeline

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load summarizer once
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarise_long_text(text, chunk_size=1000):
    words = text.split()
    summaries = []
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        summary_chunk = summarizer(chunk, max_length=150, min_length=50, do_sample=False)[0]["summary_text"]
        summaries.append(summary_chunk)
    return " ".join(summaries)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process_audio():
    file = request.files["audio"]
    input_path = os.path.join(UPLOAD_FOLDER, "lecture_input.webm")
    file.save(input_path)

    output_path = os.path.join(UPLOAD_FOLDER, "lecture.wav")
    subprocess.run(["ffmpeg", "-y", "-i", input_path, "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le", output_path],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    model_path = os.path.abspath(os.path.join("whisper.cpp", "models", "ggml-base.en.bin"))
    subprocess.run([os.path.join("whisper.cpp", "build", "bin", "Release", "whisper-cli.exe"),
                    "-m", model_path, "-f", output_path, "-otxt"])

    transcript_path = os.path.splitext(output_path)[0] + ".wav.txt"
    with open(transcript_path, "r", encoding="utf-8") as f:
        transcript = f.read()

    summary = summarise_long_text(transcript)
    return jsonify({"transcript": transcript, "summary": summary})

if __name__ == "__main__":
    app.run(debug=True)
