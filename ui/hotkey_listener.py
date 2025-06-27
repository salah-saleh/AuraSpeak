from pynput import keyboard  # For listening to global keyboard events (hotkey press/release)

class HotkeyListener:
    """
    Listens for key press and release events, triggering provided callbacks.
    """
    def __init__(self, on_press, on_release):
        self.listener = keyboard.Listener(on_press=on_press, on_release=on_release)

    def run(self):
        print("Press and hold Right Shift + Right Option to record. Release to stop and transcribe.")
        self.listener.start()
        self.listener.join() 