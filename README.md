# Voice-to-Text Agent

This project is a modular voice-to-text agent that records audio from your microphone, sends it to OpenAI's Whisper API for transcription, and can:
- Copy the result to your clipboard (polished, cleaned-up text)
- Search the web using DuckDuckGo (with Gemini-inferred query and result length)
- Read text aloud using Google Text-to-Speech (gTTS, with polished text)

## Features
- Record audio from your microphone
- Transcribe audio to text using OpenAI Whisper
- **AI-powered intent detection and text polishing using Gemini**
- Modular codebase for easy extension (e.g., Gemini, agent tools)
- **Web search tool**: Say "search the web about ..." to get web results (Gemini infers query and result length)
- **Text-to-speech tool**: Say "read this aloud ..." or "speak ..." to hear the text (Gemini polishes the text)

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
│   ├── intent.py          # Gemini-based intent detection and text polishing
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

### 3. Set your API keys
You need both an OpenAI API key and a Gemini API key:
```
export OPENAI_API_KEY="your-openai-api-key"      # For Whisper transcription
export GEMINI_API_KEY="your-gemini-api-key"      # For Gemini intent detection
```

### 4. Run the app
```
python main.py
```

## How to Use
- **Clipboard (default):** Just speak and your words will be transcribed, polished, and copied to your clipboard.
- **Web Search:** Start your speech with "search the web about ..." or "search for ..." and the agent will use Gemini to infer the best query and result length, search DuckDuckGo, and read the top result(s) aloud.
- **Text-to-Speech:** Start your speech with "read this aloud ..." or "speak ..." and the agent will polish your text and read it aloud using gTTS.
- **Hotkey:** Press and hold **Right Shift + Right Option** to record. Release to stop and transcribe.

## Gemini-based Intent Detection
- The agent uses Gemini to:
  - Detect your intent (web search, TTS, clipboard)
  - Polish and clean up your text (removes filler words, self-corrections, etc.)
  - For web search, infer the best query and whether you want a short or detailed answer (based on your question and instructions)
- Example:
  - "What time is it in Paris?" → short web search
  - "Explain the politics of the USA" → detailed web search
  - "Read this aloud, um, actually, say Hello world instead" → TTS: "Hello world"
  - "This is a note, uh, wait, make that a reminder for tomorrow" → Clipboard: "reminder for tomorrow"

## Improving Web Search Answers
- Currently, the agent reads out the summary/body of the top DuckDuckGo result(s).
- For direct questions (like "What's the temperature in Cairo?"), the answer may be embedded in the result body, not as a direct value.
- **Future improvement:** Integrate a direct answer extraction step (using Gemini or another LLM) to extract the most relevant fact from the search results and read that aloud.

## Dependencies
- `openai`: For Whisper transcription
- `sounddevice`, `scipy`, `numpy`: For audio recording and processing
- `pynput`: For hotkey listening
- `pyperclip`: For clipboard operations
- `duckduckgo-search`: For web search
- `gtts`: For text-to-speech
- `pygame`: For audio playback (cross-platform)
- `google-generativeai`: For Gemini intent detection and text polishing

## Extending the Project
- Add new transcription providers (e.g., Gemini) in the `transcription/` directory.
- Add agent tools or other features in new modules as needed.

---

Feel free to modify the script to suit your needs! 