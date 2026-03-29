"""
Kaydırılabilir mesaj alanı widget'ı.
"""

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QLabel, QScrollArea, QVBoxLayout, QWidget

from ..styles import C
from .bubble import Bubble


class ChatArea(QScrollArea):
    def __init__(self):
        super().__init__()
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setStyleSheet(
            f"QScrollArea {{ border: none; background: {C['chat_bg']}; }}"
        )

        self._body = QWidget()
        self._body.setStyleSheet(f"background: {C['chat_bg']};")
        self._lay = QVBoxLayout(self._body)
        self._lay.setAlignment(Qt.AlignTop)
        self._lay.setContentsMargins(0, 8, 0, 8)
        self._lay.setSpacing(2)
        self.setWidget(self._body)

        self._bubbles: dict[int, Bubble] = {}

    def add_bubble(
        self,
        sender: str,
        content: str,
        timestamp: str,
        is_mine: bool,
        msg_id: int = None,
    ) -> Bubble:
        b = Bubble(sender, content, timestamp, is_mine, msg_id)
        self._lay.addWidget(b)
        if msg_id:
            self._bubbles[msg_id] = b
        QTimer.singleShot(40, self._bottom)
        return b

    def add_system(self, text: str):
        lbl = QLabel(text)
        lbl.setAlignment(Qt.AlignCenter)
        lbl.setStyleSheet(f"color: {C['dim']}; font-size: 12px; padding: 6px 0;")
        self._lay.addWidget(lbl)
        QTimer.singleShot(40, self._bottom)

    def mark_read(self, msg_id: int):
        b = self._bubbles.get(msg_id)
        if b:
            b.mark_read()

    def clear_all(self):
        while self._lay.count():
            item = self._lay.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self._bubbles.clear()

    def _bottom(self):
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())
