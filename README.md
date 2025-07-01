# Voice-to-Text Agent

This project is a modular voice-to-text agent that records audio from your microphone, sends it to OpenAI's Whisper API and Google Speech-to-Text for transcription (benchmarked in parallel), and can:
- Copy the result to your clipboard (polished, cleaned-up text)
- Search the web using DuckDuckGo (with Gemini-inferred query and result length, direct answer extraction, and links only)
- Read text aloud using Google Text-to-Speech (gTTS, with polished text)
- **Interrupt and restart**: Instantly stop ongoing processing or speech and start over with a new recording
- **Graceful shutdown**: Cleanly stop the agent and save benchmarks on Ctrl+C

## Features
- Record audio from your microphone
- Transcribe audio to text using **both OpenAI Whisper and Google Speech-to-Text** (benchmarked in parallel)
- **AI-powered intent detection and text polishing using Gemini**
- Modular codebase for easy extension (e.g., Gemini, agent tools)
- **Web search tool**: Say "search the web about ..." to get web results (Gemini infers query and result length, scrapes and summarizes top links, and extracts a direct answer; only links are shown as results)
- **Text-to-speech tool**: Say "read this aloud ..." or "speak ..." to hear the text (Gemini polishes the text)
- **Built-in benchmarking**: Performance monitoring for all major operations
- **Interrupt and restart**: Press the hotkey again during processing or speech to stop and start over
- **Graceful shutdown**: Press Ctrl+C to stop the agent and save benchmarks to a file

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
│   ├── clipboard.py       # Clipboard utilities
│   └── benchmark.py       # Performance benchmarking utilities
│
├── tools/
│   ├── __init__.py
│   ├── intent.py          # Gemini-based intent detection and text polishing
│   ├── web_search.py      # Web search tool (DuckDuckGo, scraping, Gemini summarization)
│   ├── web_scraper.py     # Web page scraping (trafilatura)
│   └── text_to_speech.py  # Text-to-speech tool (gTTS)
│
├── search_results/        # Saved full web search results and summaries
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
- **Web Search:** Start your speech with "search the web about ..." or "search for ..." and the agent will use Gemini to infer the best query and result length, search DuckDuckGo, scrape and summarize the top links, extract a direct answer, and read it aloud. The full results and summary are saved in the `search_results/` directory. Only the top links are shown as results.
- **Text-to-Speech:** Start your speech with "read this aloud ..." or "speak ..." and the agent will polish your text and read it aloud using gTTS.
- **Hotkey:** Press and hold **Right Shift + Right Option** to record. Release to stop and transcribe.
- **Interrupt:** If the agent is processing or speaking, press the hotkey again to immediately stop and start a new recording.
- **Graceful shutdown:** Press Ctrl+C at any time to stop the agent, stop any ongoing speech, and save all benchmark data to a file in the `benchmarks/` directory.

## Benchmarking STT Engines
- After each recording, the audio is sent to **both OpenAI Whisper and Google Speech-to-Text in parallel**.
- The results and timings for both engines are printed side by side for easy comparison.
- The rest of the pipeline uses the Whisper result by default (you can change this in `main.py`).

## Google Cloud Speech-to-Text Setup
1. **Enable the Speech-to-Text API** in your Google Cloud project.
2. **Create a service account** and download the JSON key file.
3. Set the environment variable:
   ```
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-key.json"
   ```
4. The agent will use this key to authenticate with Google STT.

## Benchmarking

The agent includes built-in performance monitoring to help identify bottlenecks. After each interaction, a summary is printed, and on shutdown, all benchmark data is saved to a timestamped file in the `benchmarks/` directory.

### What's Measured
- **whisper_transcription**: OpenAI Whisper API call time
- **google_stt_transcription**: Google Speech-to-Text API call time
- **gemini_intent_detection**: Gemini intent detection and text polishing
- **duckduckgo_search**: DuckDuckGo search time
- **web_scraping**: Time to scrape content from web pages
- **gemini_summarization**: Gemini summarization of scraped content
- **gemini_answer_extraction**: Gemini answer extraction from summary
- **file_saving**: Time to save results to file
- **gtts_speech**: Text-to-speech generation and playback
- **total_processing**: Total time for the entire interaction

### Benchmark Output
After each interaction, you'll see timing information like:
```
[Benchmark] whisper_transcription: 1.234s
[Benchmark] google_stt_transcription: 0.567s
[Benchmark] gemini_intent_detection: 0.123s
[Benchmark] duckduckgo_search: 0.123s
[Benchmark] web_scraping: 2.345s
[Benchmark] gemini_summarization: 1.789s
[Benchmark] gemini_answer_extraction: 0.456s
[Benchmark] gtts_speech: 0.234s
[Benchmark] total_processing: 6.758s

==================================================
BENCHMARK SUMMARY
==================================================
whisper_transcription:
  Count: 1
  Average: 1.234s
  Min: 1.234s
  Max: 1.234s
  Total: 1.234s

google_stt_transcription:
  Count: 1
  Average: 0.567s
  Min: 0.567s
  Max: 0.567s
  Total: 0.567s
```

### Performance Insights
- **Web scraping** is typically the slowest operation (2-4 seconds for 3 pages)
- **Gemini API calls** (intent detection, summarization, answer extraction) take 0.5-2 seconds each
- **Whisper transcription** varies based on audio length (usually 1-3 seconds)
- **Google Speech-to-Text transcription** varies based on audio length (usually 1-3 seconds)
- **TTS generation** is relatively fast (0.2-0.5 seconds)

## Improved Web Search Process
- The agent now:
  1. Searches DuckDuckGo for your query and gets the top links.
  2. Scrapes the main content from each link using trafilatura.
  3. Summarizes all the scraped content with Gemini.
  4. Saves the full scraped text and summary to a file in `search_results/`.
  5. Asks Gemini to extract a direct, concise answer to your original question from the summary, with the answer length controlled by the intent/result_length (short, detailed, default).
  6. Reads the answer aloud using TTS.

## Gemini-based Intent Detection
- The agent uses Gemini to:
  - Detect your intent (web search, TTS, clipboard)
  - Polish and clean up your text (removes filler words, self-corrections, etc.)
  - For web search, infer the best query and whether you want a short or detailed answer (based on your question and instructions)
- Example:
  - "What time is it in Paris?" → short web search (1-2 informative sentences)
  - "Explain the politics of the USA" → detailed web search (a paragraph or two)
  - "Read this aloud, um, actually, say Hello world instead" → TTS: "Hello world"
  - "This is a note, uh, wait, make that a reminder for tomorrow" → Clipboard: "reminder for tomorrow"

## Dependencies
- `openai`: For Whisper transcription
- `sounddevice`, `scipy`, `numpy`: For audio recording and processing
- `pynput`: For hotkey listening
- `pyperclip`: For clipboard operations
- `duckduckgo-search`: For web search
- `gtts`: For text-to-speech
- `pygame`: For audio playback (cross-platform)
- `google-generativeai`: For Gemini intent detection, summarization, and answer extraction
- `trafilatura`: For robust web page scraping

## Extending the Project
- Add new transcription providers (e.g., Gemini) in the `transcription/` directory.
- Add agent tools or other features in new modules as needed.

---

Feel free to modify the script to suit your needs! 