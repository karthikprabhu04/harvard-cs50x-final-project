# Offline Lecture Summariser

**Video Demo:** [Youtube video link](https://youtu.be/KGfzC9ksOw8)


Most audio summarises require paid, online cloud-based webservers where you're data is submitted to external organisations. This summariser uses local, open-sourced tools to create an offline, private summarises for long-form audio and creates a summary after. No API calls are created, as a local model is used instead. Thus key principles that differentiate this tool are:
- **Free & Open Source** – will be released publicly soon  
- **Private** – all data is stored and processed locally  
- **Offline** – no internet connection required  



## Quick start

### 1. Clone the repository
```bash
git clone https://github.com/karthikprabhu04/harvard-cs50x-final-project
cd harvard-cs50x-final-project
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the app
```bash
python app.py
```


## How It Works

1. **Recording:**  
   The frontend uses JavaScript’s `MediaRecorder` API to capture audio from the user’s microphone. The user clicks “Start Recording” to begin and “Stop Recording” to finish.  
   The audio data is stored as chunks in memory and then sent to the Flask backend as a `.webm` file.

2. **Conversion to WAV:**  
   Once received, the Flask server saves the audio and converts it from `.webm` to `.wav` format using **FFmpeg**. WAV files are uncompressed, making them easier for machine learning models to process.

3. **Transcription:**  
   The `.wav` file is then passed to **Whisper.cpp**, an efficient C++ implementation of OpenAI’s Whisper speech-to-text model.  
   This generates a `.txt` transcript file containing the recognized speech.

4. **Summarization:**  
   The transcript is read back into Python, where it’s split into chunks (to handle long inputs).  
   Each chunk is summarized using a **Hugging Face transformer pipeline** with the `"sshleifer/distilbart-cnn-12-6g"` model — a lightweight and efficient summarization model.

5. **Display:**  
   The final transcript and summarized text are returned to the browser via JSON and displayed neatly on the page. The UI uses **Bootstrap** for styling and responsiveness.


## Files

- **`app.py`** — The Flask backend that handles routes, file uploads, FFmpeg conversion, Whisper transcription, and summarization logic.  
- **`templates/index.html`** — The main webpage, containing the layout, recording buttons, and sections for transcript and summary.  
- **`static/script.js`** — The client-side logic for recording audio, stopping it, sending it to the backend, and displaying results.  
- **`uploads/`** — Directory used for temporarily storing uploaded and converted audio files.  
- **`.gitignore`** — Ensures large and unnecessary files (like audio files, cache, and virtual environments) are excluded from version control.  


## Design Choices

- **Flask:**  
  Chosen for its simplicity and ability to serve both the web interface and backend logic in a single lightweight framework.  
- **Whisper.cpp:**  
  Used instead of the Python Whisper package for faster, more efficient, and offline transcription without large dependencies.  
- **BART-base model:**  
  Selected as a lighter alternative to BART-large to reduce memory usage while maintaining good summarization quality.  
- **Chunk-based summarization:**  
  Implemented to handle long transcripts by processing them in manageable sections and combining the results.  
- **Bootstrap UI:**  
  Provides a clean, minimal interface that works well on both desktop and mobile devices.  


## Challenges

1. **Deployment Compatibility:**  
   Running Whisper.cpp and FFmpeg on platforms like Render required custom build commands and file path adjustments.  
2. **Model Size and Load Time:**  
   The Hugging Face summarizer initially caused slow startup; switching to a smaller model improved performance.  
3. **Browser Permissions:**  
   Handling microphone access and browser compatibility for recording across different devices took testing and refinement.



## Future Improvements

- Allow users to **download transcripts and summaries** as text files.  
- Add **speaker detection** for multi-speaker lectures.  
- Introduce a **frontend progress bar** for long recordings.  
- Optimize summarization further using **distilled models** for faster performance.  




