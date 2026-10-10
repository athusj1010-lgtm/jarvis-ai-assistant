from __future__ import annotations

import webbrowser
from urllib.parse import quote_plus


class BrowserController:
    def __init__(self, default_browser: str = "chrome"):
        self.default_browser = default_browser.lower()

    def search_google(self, query: str) -> str:
        if not query:
            return "I need a search query."
        q = quote_plus(query)
        url = f"https://www.google.com/search?q={q}"
        self.open_url(url)
        return f"Searching Google for: {query}"

    def open_url(self, url: str, browser: str | None = None) -> str:
        target = (browser or self.default_browser).lower()
        browsers = {
            "chrome": "C:/Program Files/Google/Chrome/Application/chrome.exe",
            "opera": "C:/Program Files/Opera/opera.exe",
            "edge": "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",
        }

        if target in browsers:
            browser_path = browsers[target]
            try:
                import subprocess
                subprocess.Popen([browser_path, url])
                return f"Opening {url} in {target}."
            except Exception:
                pass

        webbrowser.open(url, new=2)
        return f"Opening {url} in your default browser."

    def open_youtube_search(self, query: str) -> str:
        q = quote_plus(query)
        url = f"https://www.youtube.com/results?search_query={q}"
        return self.open_url(url)


def open_browser_search(query: str, browser: str | None = None) -> str:
    controller = BrowserController(default_browser=browser or "chrome")
    return controller.search_google(query)
