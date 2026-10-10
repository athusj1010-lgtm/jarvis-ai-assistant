from __future__ import annotations

import os
import subprocess
from typing import Any

try:
    import pyttsx3
except Exception:  # pragma: no cover
    pyttsx3 = None


class TextToSpeechEngine:
    def __init__(self, voice: str = "default"):
        self.voice = voice
        self.engine = None
        if pyttsx3 is not None:
            try:
                self.engine = pyttsx3.init()
            except Exception:
                self.engine = None

    def speak(self, text: str) -> None:
        if not text:
            return
        if self.engine is not None:
            self.engine.say(text)
            self.engine.runAndWait()
            return
        try:
            if os.name == "nt":
                import win32com.client
                speaker = win32com.client.Dispatch("SAPI.SpVoice")
                speaker.Speak(text)
            else:
                subprocess.run(["say", text], check=False)
        except Exception:
            pass


def default_tts(voice: str = "default") -> TextToSpeechEngine:
    return TextToSpeechEngine(voice=voice)
