from gtts import gTTS  # For converting text to speech using Google TTS
import tempfile  # For creating a temporary file to store the audio
import os  # For file cleanup
import pygame  # For playing the generated audio file (cross-platform)


def speak_text(text, lang="en"):
    """
    Convert the given text to speech using gTTS and play it aloud using pygame.
    """
    tts = gTTS(text=text, lang=lang)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        temp_path = fp.name
        tts.save(temp_path)
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(temp_path)
        pygame.mixer.music.play()
        # Wait for playback to finish
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    finally:
        pygame.mixer.music.unload()
        os.remove(temp_path) 