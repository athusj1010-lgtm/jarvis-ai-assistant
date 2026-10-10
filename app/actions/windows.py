from __future__ import annotations

import os
import shutil
from pathlib import Path
from typing import Any


class FileManager:
    def __init__(self, desktop_path: str | None = None, documents_path: str | None = None, downloads_path: str | None = None):
        self.desktop_path = Path(desktop_path or Path.home() / "Desktop")
        self.documents_path = Path(documents_path or Path.home() / "Documents")
        self.downloads_path = Path(downloads_path or Path.home() / "Downloads")

    def create_folder(self, name: str, base_dir: str | Path | None = None) -> str:
        target_dir = Path(base_dir) if base_dir else self.desktop_path
        folder = target_dir / name
        folder.mkdir(parents=True, exist_ok=True)
        return f"Created folder: {folder}"

    def create_file(self, name: str, content: str = "", base_dir: str | Path | None = None) -> str:
        target_dir = Path(base_dir) if base_dir else self.desktop_path
        file_path = target_dir / name
        if not file_path.suffix:
            file_path = file_path.with_suffix(".txt")
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content or "", encoding="utf-8")
        return f"Created file: {file_path}"

    def rename_file(self, source: str | Path, new_name: str) -> str:
        src = Path(source)
        if not src.exists():
            raise FileNotFoundError(source)
        dest = src.with_name(new_name)
        src.rename(dest)
        return f"Renamed to {dest}"

    def move_file(self, source: str | Path, destination: str | Path) -> str:
        src = Path(source)
        dest = Path(destination)
        if not src.exists():
            raise FileNotFoundError(source)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(dest))
        return f"Moved {src} to {dest}"

    def search_files(self, pattern: str, root: str | Path | None = None) -> list[str]:
        base = Path(root) if root else self.documents_path
        matches: list[str] = []
        for path in base.rglob("*"):
            if pattern.lower() in path.name.lower():
                matches.append(str(path))
        return matches

    def find_by_extension(self, extension: str, root: str | Path | None = None) -> list[str]:
        base = Path(root) if root else self.downloads_path
        matches: list[str] = []
        for path in base.rglob(f"*.{extension.lstrip('.')}"):
            matches.append(str(path))
        return matches

    def read_text_file(self, file_path: str | Path) -> str:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(file_path)
        return path.read_text(encoding="utf-8", errors="replace")

    def open_file(self, file_path: str | Path) -> str:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(file_path)
        os.startfile(str(path))  # type: ignore[attr-defined]
        return f"Opening {path}"


def default_file_manager() -> FileManager:
    return FileManager()
