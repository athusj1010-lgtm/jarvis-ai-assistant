from __future__ import annotations

import threading
import time


class WakeWordEngine:
    def __init__(self, wake_word: str = "hey jarvis"):
        self.wake_word = wake_word.lower()
        self.enabled = True
        self.listening = False
        self._stop_event = threading.Event()

    def start(self, callback):
        self.listening = True
        self._stop_event.clear()
        thread = threading.Thread(target=self._loop, args=(callback,), daemon=True)
        thread.start()
        return thread

    def stop(self):
        self.listening = False
        self._stop_event.set()

    def _loop(self, callback):
        while self.listening and not self._stop_event.is_set():
            time.sleep(0.2)
            # In practice, use openWakeWord or a microphone-based audio pipeline here.
            # This minimal fallback keeps the app responsive and allows manual activation.
            if self.enabled:
                pass

    def is_available(self) -> bool:
        return True


def default_wakeword(wake_word: str = "hey jarvis") -> WakeWordEngine:
    return WakeWordEngine(wake_word=wake_word)
