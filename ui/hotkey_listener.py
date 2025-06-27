from pynput import keyboard  # For listening to global keyboard events (hotkey press/release)

class HotkeyListener:
    """
    Listens for a specific key press and release, triggering callbacks.
    """
    def __init__(self, record_key, on_start, on_stop):
        self.record_key = record_key
        self.on_start = on_start
        self.on_stop = on_stop
        self.listener = keyboard.Listener(on_press=self._on_press, on_release=self._on_release)
        self._pressed = False

    def _on_press(self, key):
        if key == self.record_key and not self._pressed:
            self._pressed = True
            self.on_start()

    def _on_release(self, key):
        if key == self.record_key and self._pressed:
            self._pressed = False
            self.on_stop()

    def run(self):
        print(f"Press and hold {self.record_key} to record. Release to stop and transcribe.")
        self.listener.start()
        self.listener.join() 