from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib  # type: ignore


DEFAULT_CONFIG = {
    "ai": {
        "provider": "openai",
        "model": "gpt-4o-mini",
        "api_key": "",
        "base_url": "",
        "temperature": 0.2,
    },
    "assist": {
        "wake_word": "hey jarvis",
        "voice_language": "en-US",
        "default_browser": "chrome",
        "startup_on_login": False,
        "mic_enabled": True,
        "listen_on_start": False,
    },
    "privacy": {
        "confirm_destructive_actions": True,
        "record_audio": False,
        "history_days": 30,
    },
    "paths": {
        "downloads": "",
        "documents": "",
        "desktop": "",
    },
    "permissions": {
        "allow_file_operations": True,
        "allow_browser_search": True,
        "allow_system_controls": True,
        "allow_admin_actions": False,
    },
}


@dataclass
class Settings:
    ai_provider: str = "openai"
    ai_model: str = "gpt-4o-mini"
    api_key: str = ""
    base_url: str = ""
    temperature: float = 0.2
    wake_word: str = "hey jarvis"
    voice_language: str = "en-US"
    default_browser: str = "chrome"
    startup_on_login: bool = False
    mic_enabled: bool = True
    listen_on_start: bool = False
    confirm_destructive_actions: bool = True
    record_audio: bool = False
    history_days: int = 30
    downloads_path: str = ""
    documents_path: str = ""
    desktop_path: str = ""
    allow_file_operations: bool = True
    allow_browser_search: bool = True
    allow_system_controls: bool = True
    allow_admin_actions: bool = False
    action_history: list[dict[str, Any]] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Settings":
        return cls(
            ai_provider=data.get("ai", {}).get("provider", "openai"),
            ai_model=data.get("ai", {}).get("model", "gpt-4o-mini"),
            api_key=data.get("ai", {}).get("api_key", ""),
            base_url=data.get("ai", {}).get("base_url", ""),
            temperature=data.get("ai", {}).get("temperature", 0.2),
            wake_word=data.get("assist", {}).get("wake_word", "hey jarvis"),
            voice_language=data.get("assist", {}).get("voice_language", "en-US"),
            default_browser=data.get("assist", {}).get("default_browser", "chrome"),
            startup_on_login=data.get("assist", {}).get("startup_on_login", False),
            mic_enabled=data.get("assist", {}).get("mic_enabled", True),
            listen_on_start=data.get("assist", {}).get("listen_on_start", False),
            confirm_destructive_actions=data.get("privacy", {}).get("confirm_destructive_actions", True),
            record_audio=data.get("privacy", {}).get("record_audio", False),
            history_days=data.get("privacy", {}).get("history_days", 30),
            downloads_path=data.get("paths", {}).get("downloads", ""),
            documents_path=data.get("paths", {}).get("documents", ""),
            desktop_path=data.get("paths", {}).get("desktop", ""),
            allow_file_operations=data.get("permissions", {}).get("allow_file_operations", True),
            allow_browser_search=data.get("permissions", {}).get("allow_browser_search", True),
            allow_system_controls=data.get("permissions", {}).get("allow_system_controls", True),
            allow_admin_actions=data.get("permissions", {}).get("allow_admin_actions", False),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "ai": {
                "provider": self.ai_provider,
                "model": self.ai_model,
                "api_key": self.api_key,
                "base_url": self.base_url,
                "temperature": self.temperature,
            },
            "assist": {
                "wake_word": self.wake_word,
                "voice_language": self.voice_language,
                "default_browser": self.default_browser,
                "startup_on_login": self.startup_on_login,
                "mic_enabled": self.mic_enabled,
                "listen_on_start": self.listen_on_start,
            },
            "privacy": {
                "confirm_destructive_actions": self.confirm_destructive_actions,
                "record_audio": self.record_audio,
                "history_days": self.history_days,
            },
            "paths": {
                "downloads": self.downloads_path,
                "documents": self.documents_path,
                "desktop": self.desktop_path,
            },
            "permissions": {
                "allow_file_operations": self.allow_file_operations,
                "allow_browser_search": self.allow_browser_search,
                "allow_system_controls": self.allow_system_controls,
                "allow_admin_actions": self.allow_admin_actions,
            },
        }


class SettingsManager:
    def __init__(self, config_path: str | Path | None = None):
        self.config_path = Path(config_path) if config_path else Path("config.toml")
        self.settings = self.load()

    def load(self) -> Settings:
        default = Settings.from_dict(DEFAULT_CONFIG)
        if not self.config_path.exists():
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            self.save(default)
            return default

        with self.config_path.open("rb") as fh:
            data = tomllib.load(fh)

        merged = self._deep_merge(DEFAULT_CONFIG, data)
        settings = Settings.from_dict(merged)
        self.settings = settings
        return settings

    def save(self, settings: Settings | None = None) -> None:
        target = settings or self.settings
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with self.config_path.open("wb") as fh:
            tomllib.dumps(target.to_dict())
            fh.write(self._toml_dumps(target.to_dict()).encode("utf-8"))

    def _deep_merge(self, base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
        result = dict(base)
        for key, value in override.items():
            if isinstance(value, dict) and isinstance(result.get(key), dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        return result

    @staticmethod
    def _toml_dumps(data: dict[str, Any]) -> str:
        lines: list[str] = []

        def render_table(prefix: str, value: dict[str, Any]) -> None:
            for key, val in value.items():
                if isinstance(val, dict):
                    lines.append(f"[{prefix}.{key}]")
                    render_table(f"{prefix}.{key}", val)
                else:
                    lines.append(f"{key} = {json.dumps(val) if isinstance(val, str) else val}")

        for key, value in data.items():
            if isinstance(value, dict):
                lines.append(f"[{key}]")
                render_table(key, value)
            else:
                lines.append(f"{key} = {json.dumps(value) if isinstance(value, str) else value}")
        return "\n".join(lines) + "\n"


def get_default_paths() -> dict[str, str]:
    import os
    home = Path.home()
    return {
        "downloads": str(home / "Downloads"),
        "documents": str(home / "Documents"),
        "desktop": str(home / "Desktop"),
    }


def ensure_env_file(path: str | Path = ".env") -> None:
    env_path = Path(path)
    if env_path.exists():
        return
    env_path.write_text(
        "OPENAI_API_KEY=your_api_key_here\n"
        "AI_MODEL=gpt-4o-mini\n"
        "AI_PROVIDER=openai\n"
        "DEFAULT_BROWSER=chrome\n"
        "WAKE_WORD=hey jarvis\n",
        encoding="utf-8",
    )
