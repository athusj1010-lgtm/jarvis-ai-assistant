from __future__ import annotations

from typing import Any

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QHBoxLayout, QComboBox, QCheckBox, QFormLayout, QLineEdit, QMessageBox


class MainWindow(QMainWindow):
    def __init__(self, app_ref: Any | None = None):
        super().__init__()
        self.app_ref = app_ref
        self.setWindowTitle("Jarvis AI Assistant")
        self.resize(920, 680)
        self.setStyleSheet(
            """
            QWidget { background: #0b1020; color: #e6f0ff; font-family: Segoe UI; }
            QPushButton { background: #1e3a8a; border: none; border-radius: 10px; padding: 10px 14px; }
            QPushButton:hover { background: #264ec7; }
            QTextEdit, QLineEdit, QComboBox { background: #101a2d; border: 1px solid #2a3f66; border-radius: 8px; color: #eaf4ff; }
            QLabel { color: #dfe9ff; }
            """
        )

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        header = QLabel("JARVIS Voice Assistant")
        header.setStyleSheet("font-size: 24px; font-weight: 600; color: #8ad4ff;")
        layout.addWidget(header)

        top_bar = QHBoxLayout()
        self.listen_button = QPushButton("Start Listening")
        self.pause_button = QPushButton("Pause")
        self.speak_button = QPushButton("Test Voice")
        self.status_label = QLabel("Idle")
        self.status_label.setStyleSheet("padding: 8px; border: 1px solid #2a4d7e; border-radius: 8px; color: #8df0b8;")
        top_bar.addWidget(self.listen_button)
        top_bar.addWidget(self.pause_button)
        top_bar.addWidget(self.speak_button)
        top_bar.addWidget(self.status_label, 1)
        layout.addLayout(top_bar)

        self.command_box = QTextEdit()
        self.command_box.setPlaceholderText("Assistant conversation and recognized commands will appear here...")
        self.command_box.setReadOnly(True)
        layout.addWidget(self.command_box)

        form = QFormLayout()
        self.env_key_input = QLineEdit()
        self.env_key_input.setPlaceholderText("OpenAI API key")
        self.default_browser_combo = QComboBox()
        self.default_browser_combo.addItems(["chrome", "edge", "opera", "default"])
        self.language_combo = QComboBox()
        self.language_combo.addItems(["en-US", "hi-IN"])
        self.wake_word_input = QLineEdit("hey jarvis")
        self.mic_cb = QCheckBox("Microphone enabled")
        self.mic_cb.setChecked(True)

        form.addRow("API key", self.env_key_input)
        form.addRow("Default browser", self.default_browser_combo)
        form.addRow("Voice language", self.language_combo)
        form.addRow("Wake word", self.wake_word_input)
        form.addRow("Mic status", self.mic_cb)

        layout.addLayout(form)

        self.send_button = QPushButton("Process Command")
        self.clear_history_button = QPushButton("Clear History")
        button_row = QHBoxLayout()
        button_row.addWidget(self.send_button)
        button_row.addWidget(self.clear_history_button)
        layout.addLayout(button_row)

        self.listen_button.clicked.connect(self.handle_start_listening)
        self.pause_button.clicked.connect(self.handle_pause)
        self.speak_button.clicked.connect(self.handle_test_voice)
        self.send_button.clicked.connect(self.handle_manual_command)
        self.clear_history_button.clicked.connect(self.clear_history)

    def append_message(self, message: str) -> None:
        self.command_box.append(message)
        self.command_box.ensureCursorVisible()

    def set_status(self, text: str, color: str = "#8df0b8") -> None:
        self.status_label.setText(text)
        self.status_label.setStyleSheet(f"padding: 8px; border: 1px solid #2a4d7e; border-radius: 8px; color: {color};")

    def handle_start_listening(self):
        self.set_status("Listening", "#8df0b8")
        if self.app_ref:
            self.app_ref.start_listening()

    def handle_pause(self):
        self.set_status("Paused", "#f7d66a")
        if self.app_ref:
            self.app_ref.pause_listening()

    def handle_test_voice(self):
        if self.app_ref:
            self.app_ref.test_voice()

    def handle_manual_command(self):
        if self.app_ref:
            self.app_ref.process_text(self.command_box.toPlainText().strip() or "Open Chrome")

    def clear_history(self):
        self.command_box.clear()


def create_main_window() -> MainWindow:
    return MainWindow()
