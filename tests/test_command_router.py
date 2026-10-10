$ErrorActionPreference = "Stop"
python -m pip install pyinstaller
pyinstaller --onefile --windowed --name jarvis-assistant app/main.py
Write-Host "Executable created in dist/"
