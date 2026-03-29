"""
Arka plan ağ iş parçacığı: TCP bağlantısı ve mesaj okuma/yazma.
"""

import socket

from PyQt5.QtCore import QThread, pyqtSignal

from protocol import decode_buffer, encode


class NetworkWorker(QThread):
    sig_msg = pyqtSignal(dict)
    sig_err = pyqtSignal(str)

    def __init__(self, host: str, port: int):
        super().__init__()
        self.host = host
        self.port = port
        self._sock: socket.socket | None = None
        self._running = False
        self._buf = b""

    def connect(self) -> None:
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.settimeout(5)
        self._sock.connect((self.host, self.port))
        self._sock.settimeout(None)
        self._running = True

    def send(self, data: dict) -> None:
        if self._sock and self._running:
            try:
                self._sock.sendall(encode(data))
            except Exception as e:
                self.sig_err.emit(str(e))

    def run(self) -> None:
        while self._running:
            try:
                chunk = self._sock.recv(8192)
                if not chunk:
                    break
                self._buf += chunk
                msgs, self._buf = decode_buffer(self._buf)
                for m in msgs:
                    self.sig_msg.emit(m)
            except Exception:
                break
        self._running = False
        self.sig_err.emit("Sunucu bağlantısı kesildi")

    def stop(self) -> None:
        self._running = False
        if self._sock:
            try:
                self._sock.close()
            except Exception:
                pass
