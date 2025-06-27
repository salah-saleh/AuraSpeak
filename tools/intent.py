def detect_intent(text):
    """
    Detects the user's intent from the transcribed text.
    Returns one of: 'web_search', 'tts', or 'clipboard'.
    """
    lowered = text.lower()
    if lowered.startswith("search the web about") or lowered.startswith("search for") or "search the web" in lowered:
        return "web_search"
    if lowered.startswith("read this aloud") or lowered.startswith("speak") or "read aloud" in lowered:
        return "tts"
    return "clipboard" 