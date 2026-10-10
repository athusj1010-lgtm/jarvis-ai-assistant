# Jarvis AI Assistant for Windows

A practical, modular personal AI voice assistant for Windows 10/11 with:

- wake-word activation and microphone controls
- speech-to-text and text-to-speech
- natural language command routing
- browser and app launching
- file operations and notes
- Windows system actions with safe confirmations
- offline fallback for simple commands
- PySide6 desktop interface and system tray-ready design

## Features

- Voice commands in English and Hindi-friendly routing
- Browser search in Chrome, Edge, or Opera where available
- Open apps like Chrome, Notepad, Calculator, File Explorer, Settings, etc.
- Create folders, notes, and files with voice guidance
- Ask for confirmation before destructive or irreversible actions
- AI model integration via OpenAI-compatible APIs
- A configurable command registry and action history

## Requirements

- Windows 10/11
- Python 3.11+
- Microphone
- Internet access for web searches / AI API

## Install

1. Clone or copy the project.
2. Open PowerShell in the project folder.
3. Create a venv and install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

4. Copy `.env.example` to `.env` and populate your keys:

```powershell
Copy-Item .env.example .env
```

5. Optional: edit `config.example.toml` and copy it to `config.toml`:

```powershell
Copy-Item config.example.toml config.toml
```

## Run

```powershell
python -m app.main
```

## Example Commands

- "Hey Jarvis, open Chrome"
- "Open calculator"
- "Search Google for Python tutorials"
- "Open YouTube and search for physics lectures"
- "Create a folder named AI Projects on my Desktop"
- "Create a text file named study plan"
- "Find my Python project"
- "Take a screenshot"
- "Tell me the time"
- "Open Windows Settings"
- "Lock the PC"

## Notes

- Wake-word detection in this starter version uses a lightweight compatibility layer and is designed to be extended with `openWakeWord` or a dedicated microphone audio pipeline.
- If the AI API is unavailable, the router falls back to a rule-based command parser for basic tasks.
- Destructive file operations always require explicit confirmation in the safety layer.

## Packaging as EXE

Use PyInstaller if you want a standalone Windows executable:

```powershell
pip install pyinstaller
pyinstaller --onefile --noconsole --name jarvis-assistant app/main.py
```

## Project Structure

- `app/main.py` — bootstraps the assistant
- `app/ai/router.py` — intents and command routing
- `app/actions/apps.py` — app launch and close logic
- `app/actions/browser.py` — browser and search functions
- `app/actions/files.py` — create, move, search, and read file operations
- `app/actions/windows.py` — system controls, settings, volume, screenshot, lock
- `app/speech/stt.py` — speech recognition
- `app/speech/tts.py` — text-to-speech
- `app/speech/wakeword.py` — wake-word layer
- `app/gui/main_window.py` — desktop UI
- `app/core/security.py` — permission and history controls
- `tests/` — command routing and file operation checks

## Testing

```powershell
pytest -q
```

## Safety and Privacy

- No secret credentials are exposed to the AI model.
- You can review action history in `data/action_history.json`.
- Administrative actions require explicit approval.
- Audio is not secretly recorded or transmitted.

