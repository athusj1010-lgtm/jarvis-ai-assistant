from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Any

from app.ai.client import AIClient


@dataclass
class CommandIntent:
    action: str
    target: str = ""
    details: str = ""
    args: dict[str, Any] = field(default_factory=dict)
    confidence: float = 0.0


class CommandRouter:
    def __init__(self, ai_client: AIClient | None = None):
        self.ai_client = ai_client

    def route(self, raw_text: str) -> CommandIntent:
        text = raw_text.strip()
        if not text:
            return CommandIntent(action="noop", details="No command detected.")

        lowered = text.lower()
        if self.ai_client and self.ai_client.is_available():
            try:
                result = self._ask_llm(text)
                if result:
                    return result
            except Exception:
                pass

        return self._fallback_rule_match(text, lowered)

    def _ask_llm(self, raw_text: str) -> CommandIntent:
        system_prompt = (
            "You are a safe command router for a Windows AI assistant. "
            "Return valid JSON only with keys: action, target, details, args, confidence. "
            "Allowed actions: open_app, search_web, open_website, close_app, switch_app, "
            "create_folder, create_file, find_files, read_file, tell_time, take_screenshot, "
            "set_volume, mute_audio, unmute_audio, open_settings, open_notepad, open_terminal, "
            "toggle_media, lock_pc, noop, ask_user. "
            "Do not invent unsupported actions."
        )
        response = self.ai_client.chat(system_prompt, raw_text)
        payload = json.loads(response.strip().strip("```json").strip("```"))
        return CommandIntent(
            action=payload.get("action", "noop"),
            target=payload.get("target", ""),
            details=payload.get("details", raw_text),
            args=payload.get("args", {}),
            confidence=float(payload.get("confidence", 0.5)),
        )

    def _fallback_rule_match(self, text: str, lowered: str) -> CommandIntent:
        if re.search(r"\b(open|launch)\s+(chrome|google chrome|opera|edge|notepad|calculator|file explorer|settings|task manager|command prompt|powershell|youtube|physics wallah|browser)\b", lowered):
            app = re.search(r"(chrome|google chrome|opera|edge|notepad|calculator|file explorer|settings|task manager|command prompt|powershell|youtube|physics wallah|browser)", lowered)
            target = app.group(1) if app else ""
            return CommandIntent(action="open_app", target=target, details=text, confidence=0.9)

        if "search" in lowered or "find information" in lowered or "google for" in lowered or "look up" in lowered:
            match = re.search(r"(?:search|find|look up)(?:\s+(?:google|browser|web))?\s+(?:for\s+)?(.+)", lowered)
            query = match.group(1).strip() if match else text
            return CommandIntent(action="search_web", target="google", details=query, args={"query": query}, confidence=0.85)

        if re.search(r"\b(open|launch)\s+(?:the\s+)?website\b|\bvisit\s+", lowered):
            return CommandIntent(action="open_website", target="website", details=text, confidence=0.8)

        if re.search(r"\b(close|quit|exit)\s+(chrome|notepad|calculator|file explorer|settings|task manager|edge|opera)\b", lowered):
            app = re.search(r"(chrome|notepad|calculator|file explorer|settings|task manager|edge|opera)", lowered)
            return CommandIntent(action="close_app", target=app.group(1) if app else "", details=text, confidence=0.8)

        if "switch to" in lowered or "focus" in lowered:
            app = re.search(r"(?:switch to|focus)\s+(chrome|notepad|calculator|file explorer|settings|task manager|edge|opera)", lowered)
            return CommandIntent(action="switch_app", target=app.group(1) if app else "", details=text, confidence=0.8)

        if "create a folder" in lowered or "make a folder" in lowered:
            match = re.search(r"(?:create|make)\s+(?:a\s+)?folder\s+(?:named\s+)?([\w\s.-]+)", lowered)
            folder_name = match.group(1).strip() if match else "new_folder"
            return CommandIntent(action="create_folder", target=folder_name, details=text, confidence=0.8)

        if "create a file" in lowered or "make a file" in lowered or "create note" in lowered:
            match = re.search(r"(?:create|make)\s+(?:a\s+)?(?:file|note)\s+(?:named\s+)?([\w\s.-]+)", lowered)
            file_name = match.group(1).strip() if match else "note.txt"
            return CommandIntent(action="create_file", target=file_name, details=text, confidence=0.8)

        if "find" in lowered and ("pdf" in lowered or "file" in lowered or "document" in lowered):
            return CommandIntent(action="find_files", target="documents", details=text, confidence=0.7)

        if "time" in lowered or "date" in lowered:
            return CommandIntent(action="tell_time", target="", details=text, confidence=0.9)

        if "screenshot" in lowered or "screen shot" in lowered:
            return CommandIntent(action="take_screenshot", target="", details=text, confidence=0.9)

        if "volume" in lowered or "mute" in lowered or "unmute" in lowered:
            if "mute" in lowered:
                return CommandIntent(action="mute_audio", target="", details=text, confidence=0.9)
            if "unmute" in lowered:
                return CommandIntent(action="unmute_audio", target="", details=text, confidence=0.9)
            return CommandIntent(action="set_volume", target="", details=text, args={"level": 50}, confidence=0.8)

        if "settings" in lowered:
            return CommandIntent(action="open_settings", target="", details=text, confidence=0.8)

        if "notepad" in lowered and "write" in lowered:
            return CommandIntent(action="open_notepad", target="", details=text, confidence=0.8)

        if "lock" in lowered and "pc" in lowered:
            return CommandIntent(action="lock_pc", target="", details=text, confidence=0.9)

        if "power shell" in lowered or "command prompt" in lowered:
            return CommandIntent(action="open_terminal", target="powershell" if "powershell" in lowered else "cmd", details=text, confidence=0.9)

        if "read" in lowered and "file" in lowered:
            return CommandIntent(action="read_file", target="", details=text, confidence=0.7)

        return CommandIntent(action="ask_user", target="", details="I need clarification for this request.", confidence=0.4)
