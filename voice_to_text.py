# Import necessary libraries
import sounddevice as sd  # For recording audio from the microphone
import scipy.io.wavfile as wav  # For saving audio as a WAV file
import openai  # For interacting with OpenAI's Whisper API
import os  # For accessing environment variables
from pynput import keyboard  # For listening to key events
import numpy as np  # For handling audio data
import pyperclip  # For copying text to clipboard

# Output filename for the recorded audio
FILENAME = "recorded.wav"
# Sample rate for audio recording
FS = 44100

# Set your OpenAI API key from the environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("OPENAI_API_KEY environment variable not set.")

# Global variables to manage recording state
recording = []  # List to store audio chunks
stream = None   # Audio stream object

# Key to use for recording (Right Shift is reliably capturable and easy to press)
# You can change this to another key if you prefer (e.g., keyboard.Key.f12, keyboard.Key.f19, etc.)
RECORD_KEY = keyboard.Key.shift_r

print("Press and hold Right Shift to record. Release to stop and transcribe.")


def start_recording():
    """
    Start recording audio from the microphone.
    This function initializes the audio stream and begins collecting audio data.
    """
    global stream, recording
    print("Recording...")
    recording = []  # Reset the recording buffer
    # Create an input stream with a callback to collect audio data
    stream = sd.InputStream(samplerate=FS, channels=1, dtype="int16", callback=audio_callback)
    stream.start()


def stop_recording():
    """
    Stop the audio recording, save the audio to a WAV file,
    transcribe it using OpenAI Whisper, and copy the result to the clipboard.
    """
    global stream, recording
    if stream is not None:
        stream.stop()
        stream.close()
        stream = None
    if recording:
        # Concatenate all recorded chunks into a single array
        audio = np.concatenate(recording, axis=0)
        # Save the audio to a WAV file
        wav.write(FILENAME, FS, audio)
        print(f"Recording saved as {FILENAME}")
        # Transcribe the audio file
        transcript = transcribe_audio(FILENAME)
        print("Transcription:")
        print(transcript)
        # Copy the transcript to the clipboard
        pyperclip.copy(transcript)
        print("Transcription copied to clipboard.")


def audio_callback(indata, frames, time, status):
    """
    Callback function for the audio stream.
    Appends each chunk of recorded audio data to the global recording list.
    """
    if status:
        print(status)
    recording.append(indata.copy())


def transcribe_audio(filename):
    """
    Send the recorded audio file to OpenAI Whisper for transcription.
    Returns the transcribed text.
    """
    with open(filename, "rb") as audio_file:
        transcript = openai.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    return transcript.text


def on_press(key):
    """
    Event handler for key press.
    Starts recording when the RECORD_KEY is pressed and not already recording.
    """
    if key == RECORD_KEY and not hasattr(on_press, "pressed"):
        on_press.pressed = True
        start_recording()


def on_release(key):
    """
    Event handler for key release.
    Stops recording when the RECORD_KEY is released.
    """
    if key == RECORD_KEY and hasattr(on_press, "pressed"):
        del on_press.pressed
        stop_recording()

# Start listening for key events
# The script will keep running, waiting for the user to press and release the RECORD_KEY
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join() 