import os  # For environment variables
from google.cloud import speech  # Google Speech-to-Text API
from utils.benchmark import benchmark_function  # For benchmarking

@benchmark_function("google_stt_transcription")
def transcribe_with_google_stt(filename):
    """
    Transcribe the given audio file using Google Cloud Speech-to-Text API.
    Returns the transcribed text.
    """
    # Requires GOOGLE_APPLICATION_CREDENTIALS env var to be set to the path of your service account JSON key
    client = speech.SpeechClient()
    with open(filename, "rb") as audio_file:
        content = audio_file.read()
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,
        language_code="en-US",
        enable_automatic_punctuation=True,
    )
    response = client.recognize(config=config, audio=audio)
    # Concatenate all results
    transcript = " ".join([result.alternatives[0].transcript for result in response.results])
    return transcript.strip() 