from audio.recorder import AudioRecorder         # Handles audio recording logic (start/stop, file saving)
from transcription.openai_whisper import transcribe_with_whisper  # Handles transcription using OpenAI Whisper API
from ui.hotkey_listener import HotkeyListener    # Listens for hotkey events to trigger recording
from utils.clipboard import copy_to_clipboard    # Copies text to the system clipboard
from pynput import keyboard                      # Provides key constants (e.g., right shift)
from tools.intent import detect_intent           # Detects user intent from transcript
from tools.web_search import search_duckduckgo   # Performs web search using DuckDuckGo
from tools.text_to_speech import speak_text      # Converts text to speech using gTTS

# Use right shift as the trigger key
RECORD_KEY = keyboard.Key.shift_r

def main():
    """
    Main function to run the voice-to-text agent with intent detection and tools.
    """
    recorder = AudioRecorder()

    def on_start():
        print("Recording...")
        recorder.start()

    def on_stop():
        print("Processing...")
        filename = recorder.stop()
        if filename:
            transcript = transcribe_with_whisper(filename)
            print("Transcription:")
            print(transcript)
            # Detect intent
            intent = detect_intent(transcript)
            print(f"Detected intent: {intent}")
            if intent == "web_search":
                # Remove intent phrase from query
                query = transcript.lower().replace("search the web about", "").replace("search for", "").replace("search the web", "").strip()
                print(f"Searching the web for: {query}")
                results = search_duckduckgo(query)
                if results:
                    print("Top results:")
                    for i, r in enumerate(results, 1):
                        print(f"{i}. {r['title']}\n{r['href']}\n{r['body']}\n")
                    # Optionally, read the first result aloud
                    speak_text(results[0]['body'] or results[0]['title'])
                else:
                    print("No results found.")
            elif intent == "tts":
                # Remove intent phrase from text
                to_speak = transcript.lower().replace("read this aloud", "").replace("speak", "").replace("read aloud", "").strip()
                print(f"Speaking: {to_speak}")
                speak_text(to_speak)
            else:
                copy_to_clipboard(transcript)
                print("Transcription copied to clipboard.")
        else:
            print("No audio recorded.")

    listener = HotkeyListener(RECORD_KEY, on_start, on_stop)
    listener.run()

if __name__ == "__main__":
    main() 