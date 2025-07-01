from audio.recorder import AudioRecorder         # Handles audio recording logic (start/stop, file saving)
from transcription.openai_whisper import transcribe_with_whisper  # Handles transcription using OpenAI Whisper API
from transcription.google_stt import transcribe_with_google_stt   # Handles transcription using Google Speech-to-Text
from ui.hotkey_listener import HotkeyListener    # Listens for hotkey events to trigger recording
from utils.clipboard import copy_to_clipboard    # Copies text to the system clipboard
from utils.benchmark import benchmark_block, print_benchmark_summary, benchmark_data  # For benchmarking
from pynput import keyboard                      # Provides key constants (e.g., right shift, right option)
from tools.intent import detect_intent           # Detects user intent from transcript (Gemini-based)
from tools.web_search import search_duckduckgo   # Performs web search using DuckDuckGo and Gemini
from tools.text_to_speech import speak_text, stop_speech  # Converts text to speech using gTTS
import threading  # For interruption support
import signal     # For graceful shutdown
import sys        # For sys.exit
import os         # For saving benchmark files
import datetime   # For timestamped filenames

# Use right shift + right option as the trigger key combination
RECORD_KEYS = {keyboard.Key.shift_r, keyboard.Key.alt_r}

# Global interrupt event
interrupt_event = threading.Event()

# For graceful shutdown
def save_benchmarks_to_file():
    os.makedirs("benchmarks", exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = f"benchmarks/bench_{ts}.txt"
    with open(file_path, "w") as f:
        if not benchmark_data:
            f.write("[Benchmark] No data collected.\n")
        else:
            f.write("BENCHMARK SUMMARY\n" + "="*50 + "\n")
            for name, times in benchmark_data.items():
                if times:
                    avg_time = sum(times) / len(times)
                    min_time = min(times)
                    max_time = max(times)
                    total_time = sum(times)
                    count = len(times)
                    f.write(f"{name}:\n")
                    f.write(f"  Count: {count}\n")
                    f.write(f"  Average: {avg_time:.3f}s\n")
                    f.write(f"  Min: {min_time:.3f}s\n")
                    f.write(f"  Max: {max_time:.3f}s\n")
                    f.write(f"  Total: {total_time:.3f}s\n\n")
    print(f"[Benchmark] Saved to {file_path}")

def graceful_exit(*args):
    print("\n[Shutdown] Stopping agent and saving benchmarks...")
    interrupt_event.set()
    stop_speech()
    save_benchmarks_to_file()
    sys.exit(0)

signal.signal(signal.SIGINT, graceful_exit)

def main():
    """
    Main function to run the voice-to-text agent with Gemini-based intent detection and tools.
    """
    recorder = AudioRecorder()
    pressed_keys = set()
    processing_lock = threading.Lock()
    processing_thread = [None]  # Mutable container to allow reassignment

    def process_audio(filename):
        with benchmark_block("total_processing"):
            # Run both STT engines in parallel
            whisper_result = {}
            google_result = {}
            def run_whisper():
                whisper_result["text"] = transcribe_with_whisper(filename)
            def run_google():
                google_result["text"] = transcribe_with_google_stt(filename)
            t1 = threading.Thread(target=run_whisper)
            t2 = threading.Thread(target=run_google)
            t1.start()
            t2.start()
            t1.join()
            t2.join()
            print("\n--- STT Results ---")
            print("[OpenAI Whisper]")
            print(whisper_result["text"])
            print("[Google STT]")
            print(google_result["text"])
            print("-------------------\n")
            # Use Whisper result for downstream processing (or swap to google_result["text"] to compare)
            transcript = whisper_result["text"]
            print("Transcription (using Whisper for downstream):")
            print(transcript)
            # Use Gemini to detect intent, query, and result_length
            intent_result = detect_intent(transcript)
            intent = intent_result["intent"]
            query = intent_result["query"]
            result_length = intent_result.get("result_length", "default")
            print(f"Detected intent: {intent}")
            if intent == "web_search":
                print(f"Searching the web for: {query} (result length: {result_length})")
                answer, file_path, results = search_duckduckgo(query, result_length=result_length)
                print("\nDirect answer:")
                print(answer)
                print(f"\nFull results and summary saved to: {file_path}")
                print("\nTop links:")
                for i, r in enumerate(results, 1):
                    print(f"{i}. {r['title']}\n{r['href']}\n")
                speak_text(answer, stop_event=interrupt_event)
            elif intent == "tts":
                print(f"Speaking: {query}")
                speak_text(query, stop_event=interrupt_event)
            else:
                copy_to_clipboard(query)
                print("Transcription copied to clipboard.")
        print_benchmark_summary()

    def on_start():
        if processing_lock.locked():
            print("[Interrupt] Stopping ongoing processing and starting over...")
            interrupt_event.set()
            stop_speech()
            if processing_thread[0] and processing_thread[0].is_alive():
                processing_thread[0].join(timeout=2)
            interrupt_event.clear()
        print("Recording...")
        recorder.start()

    def on_stop():
        print("Processing...")
        filename = recorder.stop()
        if filename:
            def run_processing():
                with processing_lock:
                    process_audio(filename)
            t = threading.Thread(target=run_processing)
            processing_thread[0] = t
            t.start()
        else:
            print("No audio recorded.")

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
    try:
        listener.run()
    except SystemExit:
        pass
    except Exception as e:
        print(f"[Error] {e}")
        graceful_exit()

if __name__ == "__main__":
    main() 