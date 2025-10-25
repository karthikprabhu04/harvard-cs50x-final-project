# Lecturer Audio Summariser

A privacy-first, offline app that listens to lectures, transcribes them using Whisper, and summarises the content locally — built for Harvard CS50x.

## Features

- Offline transcription using **Whisper**
- Offline summarisation using a **local LLM**
- Simple **Flask web interface**

### Key Principles
- **Free & Open Source** – will be released publicly soon  
- **Private** – all data is stored and processed locally  
- **Offline** – no internet connection required  

## Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/lecturer-audio-summariser.git
cd lecturer-audio-summariser

### 2. Install dependencies
```bash
pip install -r requirements.txt

### 3. Run the app
```bash
python app.py

### Tech Stack
- Python (Flask) – backend framework
- Whisper (GGML) – for local transcription
- Local LLM (GGUF/GGML) – for offline summarisation

