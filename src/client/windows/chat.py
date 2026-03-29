"""
Ana sohbet penceresi.
"""

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QFrame, QHBoxLayout, QLabel, QLineEdit, QMainWindow,
    QMessageBox, QPushButton, QScrollArea, QSplitter,
    QStackedWidget, QVBoxLayout, QWidget,
)

from config import ASSET_DIR, PUBLIC
from ..network import NetworkWorker
from ..styles import C, APP_QSS
from ..widgets.chat_area import ChatArea
from ..widgets.user_row import UserRow


class ChatWindow(QMainWindow):
    def __init__(self, username: str, worker: NetworkWorker):
        super().__init__()
        self.username = username
        self.net      = worker
        self.current  = PUBLIC
        self._areas: dict[str, ChatArea] = {}
        self._rows:   dict[str, UserRow]  = {}
        self._unread: dict[str, int]      = {}
        self._known_users: set[str]       = set()
        self._pending_receipts: dict[str, list] = {}

        self.setWindowTitle(f"BeQuickChat — {username}")
        self.setMinimumSize(900, 620)
        self.setStyleSheet(APP_QSS)

        icon_path = ASSET_DIR / "bequickchat.png"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))

        self._build_ui()
        self._switch(PUBLIC)

        self.net.sig_msg.connect(self._on_msg)
        self.net.sig_err.connect(self._on_err)

    # ──────────────────────── UI ──────────────────────────────

    def _build_ui(self):
        splitter = QSplitter(Qt.Horizontal)
        splitter.setHandleWidth(1)

        left = QWidget()
        left.setFixedWidth(300)
        left.setStyleSheet(f"background: {C['panel']};")
        llay = QVBoxLayout(left)
        llay.setContentsMargins(0, 0, 0, 0)
        llay.setSpacing(0)

        top_bar = QWidget()
        top_bar.setFixedHeight(56)
        top_bar.setStyleSheet(f"background: {C['header']};")
        tb_lay = QHBoxLayout(top_bar)
        tb_lay.setContentsMargins(14, 0, 10, 0)
        lbl_me = QLabel(f"  {self.username}")
        lbl_me.setStyleSheet(f"color:{C['text']}; font-size:15px; font-weight:600;")
        tb_lay.addWidget(lbl_me)
        tb_lay.addStretch()
        btn_out = QPushButton("⏻")
        btn_out.setObjectName("btn_logout")
        btn_out.setToolTip("Çıkış yap")
        btn_out.setCursor(Qt.PointingHandCursor)
        btn_out.clicked.connect(self._logout)
        tb_lay.addWidget(btn_out)
        llay.addWidget(top_bar)

        search_wrap = QWidget()
        search_wrap.setStyleSheet(f"background: {C['panel']};")
        sw_lay = QHBoxLayout(search_wrap)
        sw_lay.setContentsMargins(10, 8, 10, 8)
        self.inp_search = QLineEdit()
        self.inp_search.setPlaceholderText("🔍  Kullanıcı ara…")
        self.inp_search.textChanged.connect(self._filter_users)
        sw_lay.addWidget(self.inp_search)
        llay.addWidget(search_wrap)

        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet(f"color: {C['border']};")
        llay.addWidget(sep)

        self.user_scroll = QScrollArea()
        self.user_scroll.setWidgetResizable(True)
        self.user_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.user_scroll.setStyleSheet(
            f"QScrollArea {{ border: none; background: {C['panel']}; }}"
        )
        self.user_body = QWidget()
        self.user_body.setStyleSheet(f"background: {C['panel']};")
        self.user_lay = QVBoxLayout(self.user_body)
        self.user_lay.setContentsMargins(0, 0, 0, 0)
        self.user_lay.setSpacing(0)
        self.user_lay.setAlignment(Qt.AlignTop)
        self.user_scroll.setWidget(self.user_body)
        llay.addWidget(self.user_scroll)

        right = QWidget()
        rlay  = QVBoxLayout(right)
        rlay.setContentsMargins(0, 0, 0, 0)
        rlay.setSpacing(0)

        self.right_header = QWidget()
        self.right_header.setFixedHeight(56)
        self.right_header.setStyleSheet(f"background: {C['header']};")
        rh_lay = QHBoxLayout(self.right_header)
        rh_lay.setContentsMargins(16, 0, 16, 0)
        self.lbl_chat_name = QLabel("Genel Sohbet")
        self.lbl_chat_name.setStyleSheet(
            f"color:{C['text']}; font-size:16px; font-weight:600;"
        )
        self.lbl_chat_status = QLabel("")
        self.lbl_chat_status.setStyleSheet(f"color:{C['dim']}; font-size:12px;")
        name_col = QVBoxLayout()
        name_col.setSpacing(1)
        name_col.addWidget(self.lbl_chat_name)
        name_col.addWidget(self.lbl_chat_status)
        rh_lay.addLayout(name_col)
        rh_lay.addStretch()
        rlay.addWidget(self.right_header)

        self.stack = QStackedWidget()
        self.stack.setStyleSheet(f"background: {C['chat_bg']};")
        rlay.addWidget(self.stack)

        input_bar = QWidget()
        input_bar.setFixedHeight(66)
        input_bar.setStyleSheet(
            f"background: {C['input_bg']}; border-top: 1px solid {C['border']};"
        )
        ib_lay = QHBoxLayout(input_bar)
        ib_lay.setContentsMargins(12, 10, 12, 10)
        ib_lay.setSpacing(8)

        self.inp_msg = QLineEdit()
        self.inp_msg.setPlaceholderText("Mesaj yaz…")
        self.inp_msg.returnPressed.connect(self._send_msg)
        ib_lay.addWidget(self.inp_msg)

        btn_send = QPushButton("➤")
        btn_send.setObjectName("btn_send")
        btn_send.setCursor(Qt.PointingHandCursor)
        btn_send.clicked.connect(self._send_msg)
        ib_lay.addWidget(btn_send)
        rlay.addWidget(input_bar)

        splitter.addWidget(left)
        splitter.addWidget(right)
        splitter.setSizes([300, 700])

        container = QWidget()
        container.setObjectName("root")
        cl = QHBoxLayout(container)
        cl.setContentsMargins(0, 0, 0, 0)
        cl.addWidget(splitter)
        self.setCentralWidget(container)

        self._add_row(PUBLIC, is_group=True)

    # ──────────────────────── Satır yönetimi ─────────────────

    def _add_row(self, key: str, is_group: bool = False, online: bool = False):
        if key in self._rows:
            return
        if not is_group:
            online = key in self._known_users
        row = UserRow(key, is_group=is_group, online=online)
        row.mousePressEvent = lambda _e, k=key: self._switch(k)
        self._rows[key] = row
        self._areas[key] = area = ChatArea()
        self.stack.addWidget(area)

        if is_group:
            self.user_lay.insertWidget(0, row)
        else:
            self.user_lay.addWidget(row)

    def _switch(self, key: str):
        if key not in self._rows:
            self._add_row(key, online=key in self._known_users)

        if self.current in self._rows:
            self._rows[self.current].set_selected(False)

        self.current = key
        self._rows[key].set_selected(True)
        self._rows[key].show_badge(0)
        self._unread[key] = 0

        for mid, sender in self._pending_receipts.pop(key, []):
            self.net.send({"type": "read_receipt", "msg_id": mid, "sender": sender})

        self.stack.setCurrentWidget(self._areas[key])

        if key == PUBLIC:
            self.lbl_chat_name.setText("Genel Sohbet")
            self.lbl_chat_status.setText("")
        else:
            self.lbl_chat_name.setText(key)
            online = key in self._known_users
            color  = C["green"] if online else C["dim"]
            status = "Çevrimiçi" if online else "Çevrimdışı"
            self.lbl_chat_status.setStyleSheet(f"color:{color}; font-size:12px;")
            self.lbl_chat_status.setText(status)
            if self._areas[key]._lay.count() == 0:
                self.net.send({"type": "get_private_history", "with": key})

        self.inp_msg.setFocus()

    # ──────────────────────── Mesaj gönder ───────────────────

    def _send_msg(self):
        text = self.inp_msg.text().strip()
        if not text:
            return
        self.inp_msg.clear()

        if self.current == PUBLIC:
            self.net.send({"type": "chat", "content": text})
        else:
            self.net.send({"type": "private", "recipient": self.current, "content": text})

    # ──────────────────────── Gelen mesaj işle ───────────────

    def _on_msg(self, msg: dict):
        t = msg.get("type")

        if t == "history":
            area = self._areas[PUBLIC]
            area.clear_all()
            for m in msg["messages"]:
                is_mine = m["sender"] == self.username
                area.add_bubble(m["sender"], m["content"], m["timestamp"], is_mine, m["id"])

        elif t == "private_history":
            other = msg["with"]
            if other not in self._rows:
                self._add_row(other)
            area = self._areas[other]
            area.clear_all()
            for m in msg["messages"]:
                is_mine = m["sender"] == self.username
                area.add_bubble(m["sender"], m["content"], m["timestamp"], is_mine, m["id"])

        elif t == "chat":
            is_mine = msg["sender"] == self.username
            area = self._areas[PUBLIC]
            area.add_bubble(
                msg["sender"], msg["content"], msg["timestamp"], is_mine, msg.get("msg_id")
            )
            if not is_mine and self.current != PUBLIC:
                self._bump_unread(PUBLIC)
            if not is_mine and msg.get("msg_id") and self.current == PUBLIC:
                self.net.send({
                    "type": "read_receipt",
                    "msg_id": msg["msg_id"],
                    "sender": msg["sender"],
                })

        elif t == "private":
            sender    = msg["sender"]
            recipient = msg["recipient"]
            is_mine   = sender == self.username
            other     = recipient if is_mine else sender

            if other not in self._rows:
                self._add_row(other)

            area = self._areas[other]
            area.add_bubble(sender, msg["content"], msg["timestamp"], is_mine, msg.get("msg_id"))

            if not is_mine:
                mid = msg.get("msg_id")
                if self.current != other:
                    self._bump_unread(other)
                    if mid:
                        self._pending_receipts.setdefault(other, []).append((mid, sender))
                elif mid:
                    self.net.send({"type": "read_receipt", "msg_id": mid, "sender": sender})

        elif t == "user_list":
            self._known_users = set(msg["users"]) - {self.username}
            self._refresh_user_list()

        elif t == "system":
            for area in self._areas.values():
                area.add_system(msg["content"])

        elif t == "read_receipt":
            mid = msg.get("msg_id")
            if mid:
                for area in self._areas.values():
                    area.mark_read(mid)

    def _bump_unread(self, key: str):
        self._unread[key] = self._unread.get(key, 0) + 1
        self._rows[key].show_badge(self._unread[key])

    def _refresh_user_list(self):
        for uname, row in list(self._rows.items()):
            if uname == PUBLIC:
                continue
            row.set_online(uname in self._known_users)

        for uname in self._known_users:
            if uname not in self._rows:
                self._add_row(uname, online=True)

        if self.current != PUBLIC and self.current in self._rows:
            online = self.current in self._known_users
            color  = C["green"] if online else C["dim"]
            status = "Çevrimiçi" if online else "Çevrimdışı"
            self.lbl_chat_status.setStyleSheet(f"color:{color}; font-size:12px;")
            self.lbl_chat_status.setText(status)

    def _filter_users(self, text: str):
        text = text.lower()
        for key, row in self._rows.items():
            if key == PUBLIC:
                continue
            row.setVisible(text in key.lower())

    # ──────────────────────── Bağlantı / çıkış ───────────────

    def _on_err(self, msg: str):
        QMessageBox.critical(self, "Bağlantı Hatası", msg)
        self._logout()

    def _logout(self):
        from .login import LoginWindow  # döngüsel import'u önlemek için geç import
        self.net.stop()
        self._login = LoginWindow()
        self._login.show()
        self.close()

    def closeEvent(self, event):
        self.net.stop()
        event.accept()
