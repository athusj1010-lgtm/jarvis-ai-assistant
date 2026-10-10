from __future__ import annotations

import os
from typing import Optional

try:
    import speech_recognition as sr
except Exception:  # pragma: no cover
    sr = None


class SpeechToTextEngine:
    def __init__(self, language: str = "en-US", mic_index: int | None = None):
        self.language = language
        self.mic_index = mic_index
        self.recognizer = sr.Recognizer() if sr else None

    def listen_once(self, timeout: int = 10, phrase_time_limit: int = 5) -> str:
        if self.recognizer is None:
            raise RuntimeError("SpeechRecognition is not installed.")

        with sr.Microphone(device_index=self.mic_index) as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)

        try:
            return self.recognizer.recognize_google(audio, language=self.language)
        except sr.UnknownValueError:
            return ""
        except Exception:
            return ""

    def is_available(self) -> bool:
        return self.recognizer is not None


def default_stt(language: str = "en-US") -> SpeechToTextEngine:
    return SpeechToTextEngine(language=language)
