import sounddevice as sd     # For capturing audio from the microphone
import scipy.io.wavfile as wav  # For saving audio data as a WAV file
import numpy as np           # For handling and concatenating audio data arrays

FS = 44100  # Sample rate
FILENAME = "recorded.wav"

class AudioRecorder:
    """
    Handles audio recording from the microphone.
    """
    def __init__(self, filename=FILENAME, fs=FS):
        self.filename = filename
        self.fs = fs
        self.recording = []
        self.stream = None

    def start(self):
        """Start recording audio from the microphone."""
        self.recording = []
        self.stream = sd.InputStream(samplerate=self.fs, channels=1, dtype="int16", callback=self._callback)
        self.stream.start()

    def stop(self):
        """Stop recording, save to file, and return the filename."""
        if self.stream is not None:
            self.stream.stop()
            self.stream.close()
            self.stream = None
        if self.recording:
            audio = np.concatenate(self.recording, axis=0)
            wav.write(self.filename, self.fs, audio)
            return self.filename
        return None

    def _callback(self, indata, frames, time, status):
        """
        Callback function for the sounddevice.InputStream.

        This function is automatically called by the InputStream whenever new audio data is available.
        It receives a chunk of audio data from the microphone and appends it to the recording buffer.

        If there is a status message (e.g., an error or warning), it is printed to the console.
        The audio data is copied and stored in self.recording for later concatenation and saving.
        """
        if status:
            print(status)  # Print any errors or warnings from the audio stream
        self.recording.append(indata.copy())  # Store a copy of the audio chunk for later processing