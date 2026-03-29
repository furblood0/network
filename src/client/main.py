"""
İstemci giriş noktası: QApplication başlatma ve koyu tema.
"""

import sys

from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import QApplication

from .styles import C
from .windows.login import LoginWindow


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    pal = QPalette()
    pal.setColor(QPalette.Window,          QColor(C["bg"]))
    pal.setColor(QPalette.WindowText,      QColor(C["text"]))
    pal.setColor(QPalette.Base,            QColor(C["input_bg"]))
    pal.setColor(QPalette.AlternateBase,   QColor(C["panel"]))
    pal.setColor(QPalette.Text,            QColor(C["text"]))
    pal.setColor(QPalette.Button,          QColor(C["header"]))
    pal.setColor(QPalette.ButtonText,      QColor(C["text"]))
    pal.setColor(QPalette.Highlight,       QColor(C["green"]))
    pal.setColor(QPalette.HighlightedText, QColor("#FFFFFF"))
    app.setPalette(pal)

    win = LoginWindow()
    win.show()
    sys.exit(app.exec_())
