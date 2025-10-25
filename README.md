# Lecturer Audio Summariser

A privacy-first offline app that listens to lectures, transcribes them using Whisper, and summarises the content locally — built for Harvard CS50x.

## Features
- Offline transcription (Whisper)
- Offline summarisation (local LLM)
- Flask web interface

Key features:
  • Free (will make open-source)
    ○ Need to use local AI models
  • Private (information stored locally)
  • Offline (does not need wifi to use)

## Run Locally
```bash
pip install -r requirements.txt
python app.py