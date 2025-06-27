from audio.recorder import AudioRecorder         # Handles audio recording logic (start/stop, file saving)
from transcription.openai_whisper import transcribe_with_whisper  # Handles transcription using OpenAI Whisper API
from ui.hotkey_listener import HotkeyListener    # Listens for hotkey events to trigger recording
from utils.clipboard import copy_to_clipboard    # Copies text to the system clipboard
from pynput import keyboard                      # Provides key constants (e.g., right shift, right option)
from tools.intent import detect_intent           # Detects user intent from transcript (Gemini-based)
from tools.web_search import search_duckduckgo   # Performs web search using DuckDuckGo
from tools.text_to_speech import speak_text      # Converts text to speech using gTTS

# Use right shift + right option as the trigger key combination
RECORD_KEYS = {keyboard.Key.shift_r, keyboard.Key.alt_r}

def main():
    """
    Main function to run the voice-to-text agent with Gemini-based intent detection and tools.
    """
    recorder = AudioRecorder()
    pressed_keys = set()

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
            # Use Gemini to detect intent, query, and result_length
            intent_result = detect_intent(transcript)
            intent = intent_result["intent"]
            query = intent_result["query"]
            result_length = intent_result.get("result_length", "default")
            print(f"Detected intent: {intent}")
            if intent == "web_search":
                print(f"Searching the web for: {query} (result length: {result_length})")
                results = search_duckduckgo(query)
                if results:
                    print("Top results:")
                    for i, r in enumerate(results, 1):
                        print(f"{i}. {r['title']}\n{r['href']}\n{r['body']}\n")
                    # Optionally, read the first result aloud (short: just title/body, detailed: more)
                    if result_length == "short":
                        speak_text(results[0]['body'] or results[0]['title'])
                    else:
                        # For detailed, concatenate more results or bodies
                        detailed_text = " ".join([r['body'] or r['title'] for r in results])
                        speak_text(detailed_text)
                else:
                    print("No results found.")
            elif intent == "tts":
                print(f"Speaking: {query}")
                speak_text(query)
            else:
                copy_to_clipboard(query)
                print("Transcription copied to clipboard.")
        else:
            print("No audio recorded.")

    # Custom hotkey logic for shift+option
    def on_press(key):
        pressed_keys.add(key)
        if RECORD_KEYS.issubset(pressed_keys) and not hasattr(on_press, "pressed"):
            on_press.pressed = True
            on_start()

    def on_release(key):
        if key in pressed_keys:
            pressed_keys.remove(key)
        if hasattr(on_press, "pressed") and not RECORD_KEYS.issubset(pressed_keys):
            del on_press.pressed
            on_stop()

    listener = HotkeyListener(on_press, on_release)
    listener.run()

if __name__ == "__main__":
    main() 