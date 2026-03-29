"""
Sol panel kullanıcı satırı widget'ı.
"""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget

from ..styles import C


class UserRow(QWidget):
    def __init__(self, name: str, is_group: bool = False, online: bool = False):
        super().__init__()
        self.name = name
        self.setFixedHeight(62)
        self.setCursor(Qt.PointingHandCursor)
        self._selected = False

        lay = QHBoxLayout(self)
        lay.setContentsMargins(14, 8, 14, 8)
        lay.setSpacing(10)

        av = QLabel()
        av.setFixedSize(42, 42)
        av.setAlignment(Qt.AlignCenter)
        if is_group:
            ch, color = "#", "#128C7E"
        else:
            ch = name[0].upper() if name else "?"
            palette = [
                "#E74C3C", "#E67E22", "#2ECC71", "#1ABC9C",
                "#3498DB", "#9B59B6", "#E91E63", "#00BCD4",
            ]
            color = palette[ord(ch.lower()) % len(palette)]
        av.setText(ch)
        av.setStyleSheet(
            f"background:{color}; border-radius:21px;"
            f" color:white; font-size:16px; font-weight:bold;"
        )
        lay.addWidget(av)

        col = QVBoxLayout()
        col.setSpacing(2)
        lbl_name = QLabel("Genel Sohbet" if is_group else name)
        lbl_name.setStyleSheet(f"color:{C['text']}; font-size:15px; font-weight:500;")
        col.addWidget(lbl_name)

        if is_group:
            self._lbl_status = None
        else:
            dot    = "●" if online else "○"
            color2 = C["green"] if online else C["dim"]
            self._lbl_status = QLabel(f"{dot} {'Çevrimiçi' if online else 'Çevrimdışı'}")
            self._lbl_status.setStyleSheet(f"color:{color2}; font-size:12px;")
            col.addWidget(self._lbl_status)

        lay.addLayout(col)
        lay.addStretch()

        self.badge = QLabel("")
        self.badge.setFixedSize(20, 20)
        self.badge.setAlignment(Qt.AlignCenter)
        self.badge.setStyleSheet(
            f"background:{C['green']}; border-radius:10px;"
            f" color:white; font-size:11px; font-weight:bold;"
        )
        self.badge.hide()
        lay.addWidget(self.badge)

        self.setStyleSheet("QWidget { background: transparent; }")

    def set_selected(self, sel: bool):
        self._selected = sel
        bg = C["sel"] if sel else "transparent"
        self.setStyleSheet(f"QWidget {{ background: {bg}; }}")

    def set_online(self, online: bool):
        if self._lbl_status:
            dot   = "●" if online else "○"
            color = C["green"] if online else C["dim"]
            self._lbl_status.setText(f"{dot} {'Çevrimiçi' if online else 'Çevrimdışı'}")
            self._lbl_status.setStyleSheet(f"color:{color}; font-size:12px;")

    def show_badge(self, count: int):
        if count > 0:
            self.badge.setText(str(count) if count < 100 else "99+")
            self.badge.show()
        else:
            self.badge.hide()

    def enterEvent(self, _):
        if not self._selected:
            self.setStyleSheet(f"QWidget {{ background: {C['hover']}; }}")

    def leaveEvent(self, _):
        if not self._selected:
            self.setStyleSheet("QWidget { background: transparent; }")
