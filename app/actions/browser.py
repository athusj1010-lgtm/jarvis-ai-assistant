from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


class AppController:
    def __init__(self):
        self.known_apps = {
            "chrome": "chrome.exe",
            "google chrome": "chrome.exe",
            "opera": "opera.exe",
            "edge": "msedge.exe",
            "microsoft edge": "msedge.exe",
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "file explorer": "explorer.exe",
            "settings": "ms-settings:",
            "task manager": "taskmgr.exe",
            "command prompt": "cmd.exe",
            "powershell": "powershell.exe",
            "youtube": "https://www.youtube.com",
            "physics wallah": "https://www.physicswallah.com",
            "google": "https://www.google.com",
        }

    def open_app(self, app_name: str) -> str:
        key = app_name.lower().strip()
        if key in {"", "default"}:
            return "I need the name of the app to open."

        if key in {"chrome", "google chrome"}:
            return self._launch_by_executable("chrome.exe", "https://www.google.com")
        if key in {"opera"}:
            return self._launch_by_executable("opera.exe", "https://www.opera.com")
        if key in {"edge", "microsoft edge"}:
            return self._launch_by_executable("msedge.exe", "https://www.microsoft.com/edge")
        if key in {"notepad"}:
            return self._launch_by_executable("notepad.exe")
        if key in {"calculator"}:
            return self._launch_by_executable("calc.exe")
        if key in {"file explorer", "explorer", "file manager"}:
            return self._launch_by_executable("explorer.exe")
        if key in {"settings"}:
            return self._launch_cmd("start ms-settings:")
        if key in {"task manager"}:
            return self._launch_by_executable("taskmgr.exe")
        if key in {"command prompt", "cmd", "terminal"}:
            return self._launch_by_executable("cmd.exe")
        if key in {"powershell"}:
            return self._launch_by_executable("powershell.exe")
        if key in {"youtube"}:
            return self._open_url("https://www.youtube.com")
        if key in {"physics wallah"}:
            return self._open_url("https://www.physicswallah.com")
        if key in {"google"}:
            return self._open_url("https://www.google.com")

        path = self._resolve_registered_app(app_name)
        if path:
            subprocess.Popen([path])
            return f"Opening {app_name}."

        return self._offer_browser_or_site(app_name)

    def close_app(self, app_name: str) -> str:
        key = app_name.lower().strip()
        if not key:
            return "I need the app name to close."
        executable = {
            "chrome": "chrome.exe",
            "google chrome": "chrome.exe",
            "opera": "opera.exe",
            "edge": "msedge.exe",
            "microsoft edge": "msedge.exe",
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "task manager": "taskmgr.exe",
        }
        target = executable.get(key)
        if not target:
            return f"I don’t have a safe close action for {app_name}."
        os.system(f"taskkill /F /IM {target} >nul 2>&1")
        return f"Closed {app_name}."

    def switch_to_app(self, app_name: str) -> str:
        if not app_name:
            return "Which app should I switch to?"
        if app_name.lower() in {"chrome", "google chrome"}:
            return self._launch_by_executable("chrome.exe", "https://www.google.com")
        return self._launch_by_executable(app_name)

    def _launch_by_executable(self, target: str, url: str | None = None) -> str:
        if target.startswith("http"):
            return self._open_url(target)
        if target.startswith("ms-settings:"):
            return self._launch_cmd("start ms-settings:")

        executable = shutil.which(target)
        if not executable:
            if url:
                return self._open_url(url)
            return f"{target} is not installed on this system."

        subprocess.Popen([executable])
        return f"Opening {target}."

    def _launch_cmd(self, command: str) -> str:
        subprocess.Popen(command, shell=True)
        return "Starting requested action."

    def _open_url(self, url: str) -> str:
        import webbrowser
        webbrowser.open(url, new=2)
        return f"Opening {url}."

    def _resolve_registered_app(self, app_name: str) -> str | None:
        candidates = [
            app_name,
            app_name.lower().replace(" ", ""),
            app_name.lower().replace(" ", "-"),
        ]
        for candidate in candidates:
            path = shutil.which(candidate)
            if path:
                return path
        return None

    def _offer_browser_or_site(self, app_name: str) -> str:
        if app_name.lower() in {"physics wallah", "youtube", "google"}:
            return self._offer_website(app_name)
        return f"{app_name} is not installed. I can open its website or help you configure the app path."

    def _offer_website(self, app_name: str) -> str:
        sites = {
            "physics wallah": "https://www.physicswallah.com",
            "youtube": "https://www.youtube.com",
            "google": "https://www.google.com",
        }
        url = sites.get(app_name.lower())
        if url:
            return self._open_url(url)
        return f"I don't have a website for {app_name}."


def launch_app(app_name: str) -> str:
    return AppController().open_app(app_name)
