from pathlib import Path

APP_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = APP_ROOT.parent

__all__ = ["APP_ROOT", "PROJECT_ROOT"]
