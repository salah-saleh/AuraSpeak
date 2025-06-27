from audio.recorder import AudioRecorder         # Handles audio recording logic (start/stop, file saving)
from transcription.openai_whisper import transcribe_with_whisper  # Handles transcription using OpenAI Whisper API
from ui.hotkey_listener import HotkeyListener    # Listens for hotkey events to trigger recording
from utils.clipboard import copy_to_clipboard    # Copies text to the system clipboard
from pynput import keyboard                      # Provides key constants (e.g., right shift)

# Use right shift as the trigger key
RECORD_KEY = keyboard.Key.shift_r

def main():
    """
    Main function to run the voice-to-text agent.
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
            copy_to_clipboard(transcript)
            print("Transcription copied to clipboard.")
        else:
            print("No audio recorded.")

    listener = HotkeyListener(RECORD_KEY, on_start, on_stop)
    listener.run()

if __name__ == "__main__":
    main() 