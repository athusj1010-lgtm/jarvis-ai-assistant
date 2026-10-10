from __future__ import annotations

import ctypes
import os
import subprocess
from pathlib import Path

try:
    import pycaw  # type: ignore
except Exception:  # pragma: no cover
    pycaw = None


class WindowsController:
    def __init__(self):
        self.volume_available = pycaw is not None

    def open_settings(self) -> str:
        os.system("start ms-settings:")
        return "Opening Windows Settings."

    def lock_pc(self) -> str:
        ctypes.windll.user32.LockWorkStation()
        return "Locking the PC."

    def take_screenshot(self, save_dir: str | None = None) -> str:
        target_dir = Path(save_dir) if save_dir else Path.home() / "Pictures"
        target_dir.mkdir(parents=True, exist_ok=True)
        out = target_dir / "jarvis_screenshot.png"
        subprocess.run(["powershell", "Add-Type -AssemblyName System.Windows.Forms;", "Add-Type -AssemblyName System.Drawing;", "$screen = [System.Windows.Forms.SystemInformation]::VirtualScreen;", "$bounds = [System.Drawing.Rectangle]::FromLTRB($screen.Left, $screen.Top, $screen.Right, $screen.Bottom);", "$bitmap = New-Object System.Drawing.Bitmap $bounds.Width, $bounds.Height;", "$graphics = [System.Drawing.Graphics]::FromImage($bitmap);", "$graphics.CopyFromScreen($bounds.Location, [System.Drawing.Point]::Empty, $bounds.Size);", "$bitmap.Save('" + str(out) + "', [System.Drawing.Imaging.ImageFormat]::Png);", "$graphics.Dispose();", "$bitmap.Dispose()"], check=False)
        return f"Screenshot saved to {out}."

    def open_task_manager(self) -> str:
        subprocess.Popen(["taskmgr.exe"])
        return "Opening Task Manager."

    def set_volume(self, percent: int) -> str:
        if not self.volume_available:
            return "Volume control is unavailable in this environment."
        # pycaw is optional; use safe API if available.
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume  # type: ignore
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, 0, None)
        volume = interface.QueryInterface(IAudioEndpointVolume)
        volume.SetMasterVolumeLevelScalar(percent / 100.0, None)
        return f"Volume set to {percent}%."

    def mute_audio(self) -> str:
        if not self.volume_available:
            return "Mute control is unavailable in this environment."
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume  # type: ignore
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, 0, None)
        volume = interface.QueryInterface(IAudioEndpointVolume)
        volume.SetMute(1, None)
        return "Muted audio."

    def unmute_audio(self) -> str:
        if not self.volume_available:
            return "Unmute control is unavailable in this environment."
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume  # type: ignore
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, 0, None)
        volume = interface.QueryInterface(IAudioEndpointVolume)
        volume.SetMute(0, None)
        return "Audio unmuted."

    def tell_time(self) -> str:
        from datetime import datetime
        return datetime.now().strftime("It is %I:%M %p on %A, %B %d, %Y.")


def default_windows_controller() -> WindowsController:
    return WindowsController()
