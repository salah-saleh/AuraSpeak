# Voice-to-Text Agent

This project is a minimal voice-to-text agent that records audio from your microphone, sends it to OpenAI's Whisper API for transcription, and prints the result.

## Features
- Record audio from your microphone
- Transcribe audio to text using OpenAI Whisper

## Setup Instructions

### 1. Clone the repository
Clone this repository to your local machine.

### 2. Create a virtual environment (recommended)
```
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```
pip install -r requirements.txt
```

### 4. Set your OpenAI API key
You need an OpenAI API key to use the Whisper API. Set it as an environment variable:
```
export OPENAI_API_KEY="your-api-key-here"  # On Windows: set OPENAI_API_KEY="your-api-key-here"
```

### 5. Run the script
```
python voice_to_text.py
```

## Libraries Used
- `sounddevice`: For recording audio from your microphone.
- `scipy`: For saving the recorded audio as a WAV file.
- `openai`: For sending the audio to OpenAI's Whisper API and receiving the transcription.

## How it works
1. The script records 5 seconds of audio from your microphone.
2. It saves the audio as a WAV file.
3. The audio file is sent to OpenAI's Whisper API for transcription.
4. The transcribed text is printed in the terminal.

---

Feel free to modify the script to suit your needs! 