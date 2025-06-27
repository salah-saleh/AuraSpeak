# Import necessary libraries
import sounddevice as sd  # For recording audio from the microphone
import scipy.io.wavfile as wav  # For saving audio as a WAV file
import openai  # For interacting with OpenAI's Whisper API
import os  # For accessing environment variables

# Duration of the recording in seconds
DURATION = 5
# Sample rate (number of samples per second)
FS = 44100
# Output filename for the recorded audio
FILENAME = "recorded.wav"

# Record audio from the microphone
print("Recording for {} seconds...".format(DURATION))
# Start recording (mono channel, 16-bit integer samples)
recording = sd.rec(int(DURATION * FS), samplerate=FS, channels=1, dtype="int16")
sd.wait()  # Wait until recording is finished
# Save the recording as a WAV file
wav.write(FILENAME, FS, recording)
print("Recording saved as {}".format(FILENAME))

# Set your OpenAI API key from the environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("OPENAI_API_KEY environment variable not set.")

# Open the recorded audio file and send it to OpenAI Whisper for transcription
with open(FILENAME, "rb") as audio_file:
    transcript = openai.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
    )

# Print the transcribed text
print("Transcription:")
print(transcript.text) 