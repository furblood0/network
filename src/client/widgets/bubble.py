"""
Mesaj balonu widget'ı.
"""

from datetime import datetime

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget

from ..styles import C


def _fmt_time(ts: str) -> str:
    try:
        return datetime.fromisoformat(ts).strftime("%H:%M")
    except Exception:
        return ""


class Bubble(QWidget):
    def __init__(
        self,
        sender: str,
        content: str,
        timestamp: str,
        is_mine: bool,
        msg_id: int = None,
        parent=None,
    ):
        super().__init__(parent)
        self.msg_id  = msg_id
        self.is_mine = is_mine
        self._tick   = None

        outer = QHBoxLayout(self)
        outer.setContentsMargins(8, 2, 8, 2)

        box = QWidget()
        box.setMaximumWidth(440)
        inner = QVBoxLayout(box)
        inner.setContentsMargins(10, 7, 10, 7)
        inner.setSpacing(3)

        if not is_mine:
            lbl_name = QLabel(sender)
            lbl_name.setStyleSheet(
                f"color: {C['green']}; font-weight: bold; font-size: 12px;"
            )
            inner.addWidget(lbl_name)

        lbl_text = QLabel(content)
        lbl_text.setWordWrap(True)
        lbl_text.setTextInteractionFlags(Qt.TextSelectableByMouse)
        lbl_text.setStyleSheet(f"color: {C['text']}; font-size: 14px;")
        inner.addWidget(lbl_text)

        row = QHBoxLayout()
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(4)
        row.addStretch()

        lbl_time = QLabel(_fmt_time(timestamp))
        lbl_time.setStyleSheet(f"color: {C['dim']}; font-size: 11px;")
        row.addWidget(lbl_time)

        if is_mine:
            self._tick = QLabel("✓")
            self._tick.setStyleSheet(f"color: {C['dim']}; font-size: 11px;")
            row.addWidget(self._tick)

        inner.addLayout(row)

        bg = C["sent"] if is_mine else C["recv"]
        box.setStyleSheet(f"QWidget {{ background: {bg}; border-radius: 8px; }}")

        if is_mine:
            outer.addStretch()
            outer.addWidget(box)
        else:
            outer.addWidget(box)
            outer.addStretch()

    def mark_read(self):
        if self._tick:
            self._tick.setText("✓✓")
            self._tick.setStyleSheet(f"color: {C['blue']}; font-size: 11px;")
