"""
Giriş / kayıt ekranı.
"""

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget

from config import ASSET_DIR, DEFAULT_HOST, PORT
from ..network import NetworkWorker
from ..styles import C, LOGIN_QSS


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BeQuickChat")
        self.setFixedSize(420, 540)
        self.setStyleSheet(LOGIN_QSS)
        self._worker: NetworkWorker | None = None
        self._mode = "login"
        self._build()

    def _build(self):
        root = QVBoxLayout(self)
        root.setAlignment(Qt.AlignCenter)
        root.setContentsMargins(48, 28, 48, 28)
        root.setSpacing(0)

        logo = QLabel()
        logo_path = ASSET_DIR / "bequickchat.png"
        if logo_path.exists():
            pix = QPixmap(str(logo_path)).scaled(
                72, 72, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            logo.setPixmap(pix)
        else:
            logo.setText("💬")
            logo.setStyleSheet("font-size: 48px;")
        logo.setAlignment(Qt.AlignCenter)
        root.addWidget(logo)

        root.addSpacing(10)

        title = QLabel("BeQuickChat")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        root.addWidget(title)

        sub = QLabel("Hızlı ve güvenli mesajlaşma")
        sub.setObjectName("subtitle")
        sub.setAlignment(Qt.AlignCenter)
        root.addWidget(sub)

        root.addSpacing(24)

        root.addWidget(self._lbl("Sunucu IP"))
        root.addSpacing(4)
        self.inp_host = QLineEdit(DEFAULT_HOST)
        self.inp_host.setPlaceholderText("örn: 192.168.1.10")
        root.addWidget(self.inp_host)
        root.addSpacing(12)

        root.addWidget(self._lbl("Kullanıcı Adı"))
        root.addSpacing(4)
        self.inp_user = QLineEdit()
        self.inp_user.setPlaceholderText("Kullanıcı adınız")
        root.addWidget(self.inp_user)
        root.addSpacing(12)

        root.addWidget(self._lbl("Şifre"))
        root.addSpacing(4)
        self.inp_pass = QLineEdit()
        self.inp_pass.setEchoMode(QLineEdit.Password)
        self.inp_pass.setPlaceholderText("Şifreniz")
        root.addWidget(self.inp_pass)
        root.addSpacing(20)

        self.btn_primary = QPushButton("Giriş Yap")
        self.btn_primary.setObjectName("btn_primary")
        self.btn_primary.setCursor(Qt.PointingHandCursor)
        root.addWidget(self.btn_primary)

        root.addSpacing(10)

        self.btn_secondary = QPushButton("Hesap Oluştur")
        self.btn_secondary.setObjectName("btn_secondary")
        self.btn_secondary.setCursor(Qt.PointingHandCursor)
        root.addWidget(self.btn_secondary)

        root.addSpacing(14)

        self.lbl_status = QLabel("")
        self.lbl_status.setAlignment(Qt.AlignCenter)
        self.lbl_status.setWordWrap(True)
        self.lbl_status.setStyleSheet("font-size: 13px;")
        root.addWidget(self.lbl_status)

        self.inp_pass.returnPressed.connect(self.btn_primary.click)
        self.btn_primary.clicked.connect(self._on_primary)
        self.btn_secondary.clicked.connect(self._on_secondary)

    @staticmethod
    def _lbl(text: str) -> QLabel:
        l = QLabel(text)
        l.setProperty("class", "field")
        l.setStyleSheet(f"color: {C['dim']}; font-size: 12px;")
        return l

    def _on_primary(self):
        host = self.inp_host.text().strip() or DEFAULT_HOST
        user = self.inp_user.text().strip()
        pw   = self.inp_pass.text()

        if not user or not pw:
            self._status("Kullanıcı adı ve şifre boş olamaz", err=True)
            return

        self._set_busy(True)
        self._status("Bağlanıyor…")

        try:
            worker = NetworkWorker(host, PORT)
            worker.connect()
        except Exception as e:
            self._status(f"Bağlantı hatası: {e}", err=True)
            self._set_busy(False)
            return

        self._worker = worker
        self._worker.sig_msg.connect(self._on_msg)
        self._worker.sig_err.connect(lambda e: self._status(e, err=True))
        self._worker.start()

        if self._mode == "login":
            worker.send({"type": "login", "username": user, "password": pw})
        else:
            worker.send({"type": "register", "username": user, "password": pw})

    def _on_secondary(self):
        if self._mode == "login":
            self._mode = "register"
            self.btn_primary.setText("Kayıt Ol")
            self.btn_secondary.setText("Zaten hesabım var")
            self._status("")
        else:
            self._mode = "login"
            self.btn_primary.setText("Giriş Yap")
            self.btn_secondary.setText("Hesap Oluştur")
            self._status("")

    def _on_msg(self, msg: dict):
        t = msg.get("type")
        if t == "auth_ok":
            self._open_chat(msg["username"])
        elif t == "auth_fail":
            self._status(msg.get("reason", "Hata"), err=True)
            self._set_busy(False)
        elif t == "register_result":
            if msg.get("ok"):
                self._status("Kayıt başarılı! Şimdi giriş yapabilirsiniz.")
                self._mode = "login"
                self.btn_primary.setText("Giriş Yap")
                self.btn_secondary.setText("Hesap Oluştur")
                self._set_busy(False)
            else:
                self._status(msg.get("reason", "Hata"), err=True)
                self._set_busy(False)

    def _open_chat(self, username: str):
        from .chat import ChatWindow  # döngüsel import'u önlemek için geç import
        self._worker.sig_msg.disconnect(self._on_msg)
        self.chat = ChatWindow(username, self._worker)
        self.chat.show()
        self.hide()

    def _status(self, text: str, err: bool = False):
        color = C["red"] if err else C["green"]
        self.lbl_status.setStyleSheet(f"color: {color}; font-size: 13px;")
        self.lbl_status.setText(text)

    def _set_busy(self, busy: bool):
        self.btn_primary.setEnabled(not busy)
        self.btn_secondary.setEnabled(not busy)
        self.inp_user.setEnabled(not busy)
        self.inp_pass.setEnabled(not busy)
        self.inp_host.setEnabled(not busy)
