from gtts import gTTS  # For converting text to speech using Google TTS
import tempfile  # For creating a temporary file to store the audio
import os  # For file cleanup
import pygame  # For playing the generated audio file (cross-platform)
from utils.benchmark import benchmark_function, benchmark_block  # For benchmarking
import threading  # For interruption support

# Global variable to track if speech is playing
_speech_playing = False

@benchmark_function("gtts_speech")
def speak_text(text, lang="en", stop_event=None):
    """
    Convert the given text to speech using gTTS and play it aloud using pygame.
    If stop_event is set and triggered, stop playback immediately.
    Includes granular benchmarking for TTS generation and playback.
    """
    global _speech_playing
    with benchmark_block("gtts_generation"):
        print("Generating TTS...")
        tts = gTTS(text=text, lang=lang)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            temp_path = fp.name
            tts.save(temp_path)
    try:
        pygame.mixer.init()
        with benchmark_block("tts_playback"):
            print("Speaking answer: load ...")
            pygame.mixer.music.load(temp_path)
            print("Speaking answer: play ...")
            pygame.mixer.music.play()
            _speech_playing = True
            # Wait for playback to finish or interruption
            while pygame.mixer.music.get_busy():
                if stop_event and stop_event.is_set():
                    pygame.mixer.music.stop()
                    break
                pygame.time.Clock().tick(10)
    finally:
        _speech_playing = False
        try:
            pygame.mixer.music.unload()
        except Exception:
            pass
        os.remove(temp_path)

def stop_speech():
    """
    Stop any ongoing speech playback immediately.
    """
    global _speech_playing
    if _speech_playing:
        try:
            pygame.mixer.music.stop()
        except Exception:
            pass
        _speech_playing = False 