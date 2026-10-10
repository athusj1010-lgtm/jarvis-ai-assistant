$ErrorActionPreference = "Stop"

python -m venv .venv
. "$PSScriptRoot\..\.venv\Scripts\Activate.ps1"
python -m pip install --upgrade pip
pip install -r "$PSScriptRoot\..\requirements.txt"
if (!(Test-Path "$PSScriptRoot\..\.env")) {
    Copy-Item "$PSScriptRoot\..\.env.example" "$PSScriptRoot\..\.env"
}
if (!(Test-Path "$PSScriptRoot\..\config.toml")) {
    Copy-Item "$PSScriptRoot\..\config.example.toml" "$PSScriptRoot\..\config.toml"
}
Write-Host "Setup complete. Run: python -m app.main"
