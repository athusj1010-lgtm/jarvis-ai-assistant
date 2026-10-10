from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any


@dataclass
class Permission:
    name: str
    enabled: bool = True
    description: str = ""


@dataclass
class ActionRecord:
    timestamp: str
    action: str
    details: str
    status: str = "executed"
    user_confirmed: bool = False


class SecurityManager:
    def __init__(self, history_path: str | Path | None = None):
        self.history_path = Path(history_path) if history_path else Path("data/action_history.json")
        self.history_path.parent.mkdir(parents=True, exist_ok=True)
        self.permissions = {
            "browser_search": Permission("browser_search", True, "Allow web search and browser automation."),
            "file_operations": Permission("file_operations", True, "Allow file creation, rename, move, and search."),
            "system_controls": Permission("system_controls", True, "Allow system actions like volume and screenshots."),
            "admin_actions": Permission("admin_actions", False, "Require explicit confirmation before admin changes."),
        }
        self.history: list[ActionRecord] = self._load_history()

    def _load_history(self) -> list[ActionRecord]:
        if not self.history_path.exists():
            return []
        try:
            with self.history_path.open("r", encoding="utf-8") as fh:
                raw = json.load(fh)
            return [ActionRecord(**item) for item in raw]
        except Exception:
            return []

    def save_history(self) -> None:
        payload = [record.__dict__ for record in self.history]
        with self.history_path.open("w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2)

    def log_action(self, action: str, details: str, status: str = "executed", user_confirmed: bool = False) -> None:
        self.history.append(
            ActionRecord(
                timestamp=datetime.utcnow().isoformat(timespec="seconds"),
                action=action,
                details=details,
                status=status,
                user_confirmed=user_confirmed,
            )
        )
        self.save_history()

    def can(self, permission_name: str) -> bool:
        return self.permissions.get(permission_name, Permission(permission_name, False)).enabled

    def set_permission(self, permission_name: str, enabled: bool) -> None:
        if permission_name in self.permissions:
            self.permissions[permission_name].enabled = enabled

    def require_confirmation(self, action: str, description: str, confirm_callback: callable | None = None) -> bool:
        if self.permissions.get("admin_actions", Permission("admin_actions", False)).enabled:
            return True
        if confirm_callback is not None:
            return bool(confirm_callback())
        return False


def default_security_manager() -> SecurityManager:
    return SecurityManager()
