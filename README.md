# Voice-to-Text Agent

This project is a modular voice-to-text agent that records audio from your microphone, sends it to OpenAI's Whisper API for transcription, and copies the result to your clipboard.

## Features
- Record audio from your microphone
- Transcribe audio to text using OpenAI Whisper
- Modular codebase for easy extension (e.g., Gemini, agent tools)

## Project Structure

```
voice-text/
│
├── main.py                # Entry point for the app
├── requirements.txt
├── README.md
│
├── audio/
│   ├── __init__.py
│   └── recorder.py        # Audio recording logic
│
├── transcription/
│   ├── __init__.py
│   └── openai_whisper.py  # OpenAI Whisper transcription logic
│
├── ui/
│   ├── __init__.py
│   └── hotkey_listener.py # Key listening logic
│
├── utils/
│   ├── __init__.py
│   └── clipboard.py       # Clipboard utilities
```

## Setup Instructions

### 1. Create a virtual environment (recommended)
```
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install dependencies
```
pip install -r requirements.txt
```

### 3. Set your OpenAI API key
You need an OpenAI API key to use the Whisper API. Set it as an environment variable:
```
export OPENAI_API_KEY="your-api-key-here"  # On Windows: set OPENAI_API_KEY="your-api-key-here"
```

### 4. Run the app
```
python main.py
```

## How it works
1. Press and hold the Right Shift key to start recording.
2. Release the Right Shift key to stop recording and transcribe.
3. The transcript is printed and copied to your clipboard for easy pasting.

## Extending the Project
- Add new transcription providers (e.g., Gemini) in the `transcription/` directory.
- Add agent tools or other features in new modules as needed.

---

Feel free to modify the script to suit your needs! 