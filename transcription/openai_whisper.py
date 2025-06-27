import openai                # For interacting with OpenAI's Whisper API for transcription
import os                    # For accessing environment variables (API key)

openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("OPENAI_API_KEY environment variable not set.")

def transcribe_with_whisper(filename):
    """
    Transcribe the given audio file using OpenAI Whisper API.
    Returns the transcribed text.
    """
    with open(filename, "rb") as audio_file:
        transcript = openai.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    return transcript.text 