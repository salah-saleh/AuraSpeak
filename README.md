# Voice-to-Text Agent

This project is a modular voice-to-text agent that records audio from your microphone, sends it to OpenAI's Whisper API for transcription, and can:
- Copy the result to your clipboard
- Search the web using DuckDuckGo
- Read text aloud using Google Text-to-Speech (gTTS)

## Features
- Record audio from your microphone
- Transcribe audio to text using OpenAI Whisper
- Modular codebase for easy extension (e.g., Gemini, agent tools)
- **Web search tool**: Say "search the web about ..." to get web results
- **Text-to-speech tool**: Say "read this aloud ..." or "speak ..." to hear the text

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
│
├── tools/
│   ├── __init__.py
│   ├── intent.py          # Intent detection logic
│   ├── web_search.py      # Web search tool (DuckDuckGo)
│   └── text_to_speech.py  # Text-to-speech tool (gTTS)
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

## How to Use
- **Clipboard (default):** Just speak and your words will be transcribed and copied to your clipboard.
- **Web Search:** Start your speech with "search the web about ..." or "search for ..." and the agent will search DuckDuckGo and read the top result.
- **Text-to-Speech:** Start your speech with "read this aloud ..." or "speak ..." and the agent will read your text aloud using gTTS.

## Dependencies
- `openai`: For Whisper transcription
- `sounddevice`, `scipy`, `numpy`: For audio recording and processing
- `pynput`: For hotkey listening
- `pyperclip`: For clipboard operations
- `duckduckgo-search`: For web search
- `gtts`: For text-to-speech
- `pygame`: For audio playback (cross-platform)

## Extending the Project
- Add new transcription providers (e.g., Gemini) in the `transcription/` directory.
- Add agent tools or other features in new modules as needed.

---

Feel free to modify the script to suit your needs! 