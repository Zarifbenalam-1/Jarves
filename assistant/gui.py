# gui.py
# PyQt6 GUI for Jarvis-X with AI Model Selector

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QComboBox, QLabel, QVBoxLayout, QWidget
from PyQt6.QtGui import QFont, QColor, QPalette
import os

# List of available models (could be loaded from config or env)
AVAILABLE_MODELS = [
    "GPT-3.5 Turbo (OpenRouter)",
    "Mixtral 8x7B (OpenRouter)",
    "Llama-3 (OpenRouter)",
    "Gemini (OpenRouter)",
    "Phi-3 Mini (Local)",
    "TinyLlama (Local)",
    "Llama-2 7B (Local)"
]

class JarvisXGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Jarvis-X: Iron Man AI Assistant")
        self.setGeometry(100, 100, 500, 200)
        self.set_dark_theme()
        self.selected_model = AVAILABLE_MODELS[0]
        self.init_ui()

    def set_dark_theme(self):
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(30, 30, 30))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(220, 220, 220))
        palette.setColor(QPalette.ColorRole.Base, QColor(45, 45, 45))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(30, 30, 30))
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 220))
        palette.setColor(QPalette.ColorRole.ToolTipText, QColor(0, 0, 0))
        palette.setColor(QPalette.ColorRole.Text, QColor(220, 220, 220))
        palette.setColor(QPalette.ColorRole.Button, QColor(45, 45, 45))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(220, 220, 220))
        palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 0, 0))
        self.setPalette(palette)

    def init_ui(self):
        layout = QVBoxLayout()
        label = QLabel("Select AI Model:")
        label.setFont(QFont("Arial", 14))
        self.model_selector = QComboBox()
        self.model_selector.addItems(AVAILABLE_MODELS)
        self.model_selector.setCurrentIndex(0)
        self.model_selector.currentIndexChanged.connect(self.model_changed)
        self.status_label = QLabel(f"Current Model: {self.selected_model}")
        self.status_label.setFont(QFont("Arial", 12))
        layout.addWidget(label)
        layout.addWidget(self.model_selector)
        layout.addWidget(self.status_label)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def model_changed(self, index):
        self.selected_model = self.model_selector.currentText()
        self.status_label.setText(f"Current Model: {self.selected_model}")
        # Here you would trigger the backend to switch models

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = JarvisXGUI()
    window.show()
    sys.exit(app.exec())
