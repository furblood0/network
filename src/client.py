import sys
import socket
import threading
import time
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QPushButton,
    QLabel, QListWidget, QComboBox, QSizePolicy, QDialog, QFormLayout, QDialogButtonBox, QTabWidget, QTabBar, QMenuBar, QAction, QMessageBox, QScrollArea
)
from PyQt5.QtCore import Qt, pyqtSignal, QObject, QMetaObject, Q_ARG
from protocol import decode_user_list, encode_message, decode_message, decode_system_message, encode_ack, decode_ack, encode_private_message, decode_private_message, encrypt_message, decrypt_message
from time import strftime

DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 8000

QSS = '''
QWidget {
    background: #fff;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 13px;
}
QMenuBar {
    background: #fff;
    font-size: 16px;
    padding: 8px 16px;
    border: none;
    border-bottom: 3px solid #2196F3;
}
QMenuBar::item {
    background: transparent;
    color: #222;
    padding: 6px 24px;
}
QMenuBar::item:selected {
    background: #E3F2FD;
    color: #1565C0;
}
QTabBar::tab {
    background: #fff;
    color: #222;
    border: none;
    border-bottom: 3px solid transparent;
    padding: 10px 32px 8px 28px;
    font-weight: bold;
    font-size: 15px;
    border-radius: 0;
}
QTabBar::tab:selected {
    color: #1565C0;
    border-bottom: 3px solid #2196F3;
    background: #fff;
}
QTabBar::close-button {
    image: url(assets/close.png);
    subcontrol-position: right;
    subcontrol-origin: padding;
    right: 2px;
    border-radius: 2px;
}
QTabBar::close-button:hover {
    background: #E3F2FD;
}
QTabWidget::pane {
    border: 1px solid #E0E0E0;
    border-radius: 8px;
}
QScrollArea {
    border: none;
}
QPushButton {
    background-color: #2196F3;
    color: white;
    border-radius: 8px;
    padding: 8px 20px;
}
QPushButton:hover {
    background-color: #1976D2;
}
QLabel#user_list_label {
    color: #1565C0;
    font-weight: bold;
    font-size: 15px;
    padding: 4px 0 8px 0;
}
QListWidget {
    border: 1px solid #E0E0E0;
    border-radius: 8px;
    font-size: 18px;
}
QListWidget::item {
    padding: 8px 12px;
    border-bottom: 1px solid #f0f0f0;
}
QListWidget::item:hover {
    background-color: #f5f5f5;
}
QListWidget::item:selected {
    background-color: #E3F2FD;
    color: #1565C0;
    font-weight: bold;
}

/* Scrollbar Tasarımı */
QScrollBar:vertical {
    border: none;
    background: transparent; /* Arka planı şeffaf yap */
    width: 8px;
    margin: 0;
}
QScrollBar::handle:vertical {
    background: #dcdcdc; /* Tutamaç rengi */
    min-height: 20px;
    border-radius: 4px;
}
QScrollBar::handle:vertical:hover {
    background: #c0c0c0; /* Fare üzerine gelince renk */
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    border: none;
    background: none;
}
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: none;
}
QLabel#user_label {
    color: #222;
    font-weight: bold;
    font-size: 15px;
}

/* Login Panel Modern Stili */
#LoginPanel {
    background: #fff;
    border-radius: 18px;
    border: 1.5px solid #e0e0e0;
    padding: 32px 32px 24px 32px;
}
#LoginTitle {
    font-size: 22px;
    font-weight: bold;
    color: #1565C0;
    margin-bottom: 18px;
}
QLineEdit {
    border: 1.5px solid #bdbdbd;
    border-radius: 8px;
    padding: 10px 14px;
    font-size: 16px;
    background: #fafbfc;
}
QLineEdit:focus {
    border: 1.5px solid #2196F3;
    background: #fff;
}
QDialogButtonBox QPushButton, QPushButton#connect_btn {
    background-color: #2196F3;
    color: white;
    border-radius: 8px;
    padding: 10px 0;
    font-size: 16px;
    min-width: 110px;
}
QDialogButtonBox QPushButton:hover, QPushButton#connect_btn:hover {
    background-color: #1976D2;
}
QPushButton#cancel_btn {
    background: #f5f5f5;
    color: #444;
    border-radius: 8px;
    border: 1.5px solid #e0e0e0;
    font-size: 16px;
    min-width: 110px;
    padding: 10px 0;
}
QPushButton#cancel_btn:hover {
    background: #e0e0e0;
}
'''

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowTitle("BeQuickChat")
        self.setModal(True)
        self.username = None
        self.host = None
        self.port = None
        self.init_ui()

    def init_ui(self):
        self.resize(380, 320)
        # Main panel
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)
        panel = QWidget()
        panel.setObjectName("LoginPanel")
        panel_layout = QVBoxLayout(panel)
        panel_layout.setAlignment(Qt.AlignCenter)
        # Title
        title = QLabel("Sign In")
        title.setObjectName("LoginTitle")
        title.setAlignment(Qt.AlignCenter)
        panel_layout.addWidget(title)
        # Form fields
        form_layout = QFormLayout()
        form_layout.setFormAlignment(Qt.AlignCenter)
        input_width = 240
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setMinimumWidth(input_width)
        self.username_input.setMaximumWidth(input_width)
        self.host_input = QLineEdit()
        self.host_input.setText("localhost")
        self.host_input.setMinimumWidth(input_width)
        self.host_input.setMaximumWidth(input_width)
        self.port_input = QLineEdit()
        self.port_input.setText(str(DEFAULT_PORT))
        self.port_input.setReadOnly(True)
        self.port_input.setMinimumWidth(input_width)
        self.port_input.setMaximumWidth(input_width)
        form_layout.addRow("Username:", self.username_input)
        form_layout.addRow("Server:", self.host_input)
        form_layout.addRow("Port:", self.port_input)
        panel_layout.addLayout(form_layout)
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)
        self.connect_btn = QPushButton("Connect")
        self.connect_btn.setObjectName("connect_btn")
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setObjectName("cancel_btn")
        button_layout.addWidget(self.connect_btn)
        button_layout.addWidget(self.cancel_btn)
        panel_layout.addSpacing(10)
        panel_layout.addLayout(button_layout)
        main_layout.addWidget(panel, alignment=Qt.AlignCenter)
        self.connect_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)

    def accept(self):
        username = self.username_input.text().strip()
        host = self.host_input.text().strip()
        port = self.port_input.text().strip()
        if not username:
            self.username_input.setFocus()
            return
        self.username = username
        self.host = host if host else DEFAULT_HOST
        try:
            self.port = int(port)
        except ValueError:
            self.port = DEFAULT_PORT
        super().accept()

class Communicate(QObject):
    user_list_received = pyqtSignal(list)
    open_private_tab_signal = pyqtSignal(str, str, str, str)  # from_user, msg, timestamp, direction
    add_chat_bubble_signal = pyqtSignal(str, str, bool)  # text, timestamp, is_own
    add_system_message_signal = pyqtSignal(str, str)  # text, timestamp

class ChatBubble(QWidget):
    def __init__(self, text, timestamp, is_own=False):
        super().__init__()
        self.label = QLabel(text)
        self.label.setTextFormat(Qt.PlainText)
        self.label.setWordWrap(True)
        self.label.setMaximumWidth(700)
        self.label.setMinimumWidth(120)
        self.label.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        if is_own:
            bubble_color = "#F0F0F0"  # Açık gri
        else:
            bubble_color = "#DCF8C6"  # Açık yeşil
        self.label.setStyleSheet(f"""
            background-color: {bubble_color};
            border-radius: 12px;
            padding: 12px 18px;
            color: #222;
            font-size: 15px;
            max-width: 700px;
        """)
        self.time_label = QLabel(timestamp)
        self.time_label.setStyleSheet("color: #888; font-size: 11px; margin-top: 2px;")
        self.time_label.setAlignment(Qt.AlignLeft if is_own else Qt.AlignRight)
        vbox = QVBoxLayout()
        vbox.addWidget(self.label)
        vbox.addWidget(self.time_label)
        vbox.setContentsMargins(0, 0, 0, 0)
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        if is_own:
            hbox.addLayout(vbox)
            hbox.addStretch()
            hbox.setAlignment(Qt.AlignLeft)
        else:
            hbox.addStretch()
            hbox.addLayout(vbox)
            hbox.setAlignment(Qt.AlignRight)
        self.setLayout(hbox)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setMaximumWidth(370)

class ChatClientUI(QWidget):
    """
    PyQt5 multi-user UDP chat client with modern UI.
    """
    def __init__(self, username="User", host=DEFAULT_HOST, port=DEFAULT_PORT):
        """Initialize the chat client UI, socket, and background listener."""
        super().__init__()
        self.username = username
        self.host = host
        self.port = port
        self.init_ui()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('', 0))
        self.server_addr = (self.host, self.port)
        self.comm = Communicate()
        self.comm.user_list_received.connect(self.update_user_list)
        self.comm.open_private_tab_signal.connect(self.show_private_message)
        self.comm.add_chat_bubble_signal.connect(self.add_chat_bubble)
        self.comm.add_system_message_signal.connect(self.add_system_message)
        self.running = True
        self.listen_thread = threading.Thread(target=self.listen_server, daemon=True)
        self.listen_thread.start()
        self.send_join()
        self.seq = 1
        self.last_seen_seq = set()
        self.seen_system_seqs = set()
        self.private_tabs = {}

    def init_ui(self):
        """Set up the main window layout, menu, chat tabs, and user list."""
        self.setWindowTitle(f"BeQuickChat - {self.username}")
        self.resize(800, 500)
        # Menu bar
        self.menu_bar = QMenuBar(self)
        settings_menu = self.menu_bar.addMenu("Settings")
        account_action = QAction("Account Info", self)
        settings_menu.addAction(account_action)
        account_action.triggered.connect(self.show_account_info)
        # Layout with menu bar
        self.layout = QVBoxLayout()
        self.layout.setMenuBar(self.menu_bar)
        self.main_hbox = QHBoxLayout()
        # Tabbed chat area
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(False)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self.update_tab_close_button)
        self.tabs.setMovable(True)
        # General chat tab
        self.general_chat_area = QScrollArea()
        self.general_chat_area.setWidgetResizable(True)
        self.general_chat_widget = QWidget()
        self.general_chat_layout = QVBoxLayout()
        self.general_chat_layout.addStretch(1)
        self.general_chat_widget.setLayout(self.general_chat_layout)
        self.general_chat_area.setWidget(self.general_chat_widget)
        self.tabs.addTab(self.general_chat_area, "   General Chat   ")
        self.tabs.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.main_hbox.addWidget(self.tabs, 3)
        # User list (right)
        self.user_list_vbox = QVBoxLayout()
        self.user_list_label = QLabel("Users")
        self.user_list_label.setObjectName("user_list_label")
        self.user_list_label.setAlignment(Qt.AlignCenter)
        self.user_list_vbox.addWidget(self.user_list_label)
        self.user_list = QListWidget()
        self.user_list.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.user_list.itemDoubleClicked.connect(self.open_private_tab)
        self.user_list_vbox.addWidget(self.user_list)
        self.main_hbox.addLayout(self.user_list_vbox, 1)
        # Bottom: message box, send button, channel selector
        self.bottom_hbox = QHBoxLayout()
        self.bottom_hbox.setSpacing(8)
        self.bottom_hbox.setAlignment(Qt.AlignLeft)
        self.input_container = QWidget()
        self.input_hbox = QHBoxLayout()
        self.input_hbox.setContentsMargins(0, 0, 0, 0)
        self.input_hbox.setSpacing(8)
        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Type your message...")
        self.message_input.setMinimumHeight(44)
        self.message_input.setMaximumHeight(44)
        self.message_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.input_hbox.addWidget(self.message_input, 10)
        self.send_button = QPushButton("Send")
        self.send_button.setFixedSize(110, 44)
        self.input_hbox.addWidget(self.send_button, 0)
        self.input_container.setLayout(self.input_hbox)
        self.input_container.setFixedWidth(self.tabs.width())
        self.bottom_hbox.addWidget(self.input_container, 0)
        self.channel_select = QComboBox()
        self.channel_select.addItems(["UDP"])
        self.channel_select.setCurrentIndex(0)
        self.channel_select.setMinimumHeight(44)
        self.channel_select.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.bottom_hbox.addWidget(self.channel_select, 1)
        self.status_label = QLabel(f"Connection Status: {self.host}:{self.port}")
        self.status_label.setAlignment(Qt.AlignLeft)
        self.status_label.setStyleSheet("color: gray;")
        self.layout.addLayout(self.main_hbox)
        self.layout.addLayout(self.bottom_hbox)
        self.layout.addWidget(self.status_label)
        self.setLayout(self.layout)
        self.message_input.returnPressed.connect(self.on_send)
        self.send_button.clicked.connect(self.on_send)
        self.message_input.setFocus()

    def resizeEvent(self, event):
        """Handle window resize events for responsive UI."""
        super().resizeEvent(event)
        # Sohbet kutusunun genişliğini input_container'a uygula
        self.input_container.setFixedWidth(self.tabs.width())

    def open_private_tab(self, item):
        """Open a new private chat tab when a user is double-clicked."""
        user = item.text()
        if user == self.username:
            return  # No private message to self
        if user in self.private_tabs:
            self.tabs.setCurrentIndex(self.private_tabs[user])
            self.update_tab_close_button(self.private_tabs[user])
            return
        # Baloncuklu özel sohbet alanı
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        chat_widget = QWidget()
        chat_layout = QVBoxLayout()
        chat_layout.addStretch(1)
        chat_widget.setLayout(chat_layout)
        scroll.setWidget(chat_widget)
        idx = self.tabs.addTab(scroll, user)
        self.private_tabs[user] = idx
        # Her sekmeye chat_layout referansı ekle
        self.tabs.widget(idx).chat_layout = chat_layout
        self.tabs.widget(idx).chat_area = scroll
        self.tabs.setCurrentIndex(idx)
        self.update_tab_close_button(idx)

    def close_tab(self, index):
        """Close the selected chat tab."""
        if index == 0:
            return  # General chat tab cannot be closed
        user = self.tabs.tabText(index)
        self.tabs.removeTab(index)
        if user in self.private_tabs:
            del self.private_tabs[user]
        # Sekme indexleri güncellenmeli
        self.private_tabs = {u: i for u, i in self.private_tabs.items() if i != index}
        for u in list(self.private_tabs):
            if self.private_tabs[u] > index:
                self.private_tabs[u] -= 1
        self.update_tab_close_button(self.tabs.currentIndex())

    def update_tab_close_button(self, idx):
        """Update the close button visibility for tabs."""
        if idx == 0:
            self.tabs.setTabsClosable(False)
        else:
            self.tabs.setTabsClosable(True)

    def send_join(self):
        """Send a join message to the server when connecting."""
        join_msg = encode_message(self.username, "", seq=0, msg_type="join")
        self.sock.sendto(encrypt_message(join_msg), self.server_addr)

    def reliable_send(self, msg, seq, max_retries=5, timeout=1.0):
        """Send a message reliably, retrying until ACK is received or max retries reached."""
        ack_received = threading.Event()
        def wait_for_ack():
            while not ack_received.is_set() and self.running:
                try:
                    data, _ = self.sock.recvfrom(4096)
                    try:
                        data = decrypt_message(data)
                    except Exception:
                        pass
                    ack_seq = decode_ack(data)
                    if ack_seq == seq:
                        ack_received.set()
                        break
                except:
                    break
        ack_thread = threading.Thread(target=wait_for_ack, daemon=True)
        ack_thread.start()
        for _ in range(max_retries):
            if ack_received.is_set():
                break
            self.sock.sendto(encrypt_message(msg), self.server_addr)
            time.sleep(timeout)
        ack_received.set()  # Thread'i sonlandır

    def show_private_message(self, from_user, priv_msg, priv_timestamp, direction):
        """Display a private message in the appropriate tab."""
        if from_user not in self.private_tabs:
            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            chat_widget = QWidget()
            chat_layout = QVBoxLayout()
            chat_layout.addStretch(1)
            chat_widget.setLayout(chat_layout)
            scroll.setWidget(chat_widget)
            idx = self.tabs.addTab(scroll, from_user)
            self.private_tabs[from_user] = idx
            self.tabs.widget(idx).chat_layout = chat_layout
            self.tabs.widget(idx).chat_area = scroll
            self.tabs.setTabsClosable(True)
        idx = self.private_tabs[from_user]
        chat_layout = self.tabs.widget(idx).chat_layout
        chat_area = self.tabs.widget(idx).chat_area
        t = priv_timestamp if priv_timestamp else "--:--:--"
        bubble = ChatBubble(f"{from_user if direction == 'from' else 'You'}: {priv_msg}", t, direction != "from")
        container = QWidget()
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        if direction == "from":
            hbox.addWidget(bubble, 0, Qt.AlignRight)
        else:
            hbox.addWidget(bubble, 0, Qt.AlignLeft)
        container.setLayout(hbox)
        chat_layout.insertWidget(chat_layout.count()-1, container)
        chat_area.verticalScrollBar().setValue(chat_area.verticalScrollBar().maximum())

    def add_chat_bubble(self, text, timestamp, is_own=False):
        """Add a chat bubble to the chat area (own or others' message)."""
        bubble = ChatBubble(text, timestamp, is_own)
        container = QWidget()
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        if is_own:
            hbox.addWidget(bubble, 0, Qt.AlignLeft)
        else:
            hbox.addWidget(bubble, 0, Qt.AlignRight)
        container.setLayout(hbox)
        self.general_chat_layout.insertWidget(self.general_chat_layout.count()-1, container)
        self.general_chat_area.verticalScrollBar().setValue(self.general_chat_area.verticalScrollBar().maximum())

    def add_system_message(self, text, timestamp):
        """Display a system message in the chat area."""
        label = QLabel(f'<span style="color: #2e8b57;">[{timestamp}] System: {text}</span>')
        label.setTextFormat(Qt.RichText)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("background: none; border: none; font-size: 13px; margin: 6px 0 6px 0;")
        self.general_chat_layout.insertWidget(self.general_chat_layout.count()-1, label)
        self.general_chat_area.verticalScrollBar().setValue(self.general_chat_area.verticalScrollBar().maximum())

    def on_send(self):
        """Handle the send button click or Enter key to send a message."""
        msg = self.message_input.text().strip()
        channel = self.channel_select.currentText()
        if not msg:
            return
        timestamp = time.strftime('%H:%M:%S')
        seq = self.seq
        current_idx = self.tabs.currentIndex()
        if current_idx == 0:
            data = encode_message(self.username, msg, seq=seq, msg_type="chat", timestamp=timestamp)
            threading.Thread(target=self.reliable_send, args=(data, seq), daemon=True).start()
            self.comm.add_chat_bubble_signal.emit(f"You: {msg}", timestamp, True)
        else:
            user = self.tabs.tabText(current_idx)
            data = encode_private_message(self.username, user, msg, seq=seq, timestamp=timestamp)
            threading.Thread(target=self.reliable_send, args=(data, seq), daemon=True).start()
            self.comm.open_private_tab_signal.emit(user, msg, timestamp, "to")
        self.seq += 1
        self.message_input.clear()

    def listen_server(self):
        """Background thread: listen for incoming messages from the server."""
        while self.running:
            try:
                data, addr = self.sock.recvfrom(4096)
                try:
                    data = decrypt_message(data)
                except Exception:
                    pass
                ack_seq = decode_ack(data)
                if ack_seq is not None:
                    continue
                users = decode_user_list(data)
                if users:
                    self.comm.user_list_received.emit(users)
                else:
                    timestamp, sysmsg, sysseq = decode_system_message(data)
                    if sysmsg:
                        if sysseq in self.seen_system_seqs:
                            continue
                        self.seen_system_seqs.add(sysseq)
                        self.comm.add_system_message_signal.emit(sysmsg, timestamp)
                        continue
                    from_user, to_user, priv_msg, priv_seq, priv_timestamp = decode_private_message(data)
                    if from_user and to_user and priv_msg:
                        if (from_user, priv_seq) in self.last_seen_seq:
                            continue
                        self.last_seen_seq.add((from_user, priv_seq))
                        ack = encode_ack(priv_seq)
                        self.sock.sendto(encrypt_message(ack), addr)
                        self.comm.open_private_tab_signal.emit(from_user, priv_msg, priv_timestamp, "from")
                        continue
                    username, message, seq, msg_type, msg_timestamp = decode_message(data)
                    if msg_type == "chat" and username and message:
                        if (username, seq) in self.last_seen_seq:
                            continue
                        self.last_seen_seq.add((username, seq))
                        ack = encode_ack(seq)
                        self.sock.sendto(encrypt_message(ack), addr)
                        t = msg_timestamp if msg_timestamp else "--:--:--"
                        if username == self.username:
                            # Kendi mesajını tekrar baloncuk olarak ekleme
                            pass
                        else:
                            self.comm.add_chat_bubble_signal.emit(f"{username}: {message}", t, False)
            except:
                break

    def update_user_list(self, users):
        """Update the user list widget with currently online users."""
        self.user_list.clear()
        for user in users:
            self.user_list.addItem(user)

    def closeEvent(self, event):
        """Handle the window close event, send leave message, and clean up."""
        leave_msg = encode_message(self.username, "", seq=0, msg_type="leave")
        self.sock.sendto(encrypt_message(leave_msg), self.server_addr)
        self.running = False
        self.sock.close()
        event.accept()

    def show_account_info(self):
        """Show the account information dialog."""
        info = f"Username: {self.username}\nServer: {self.host}\nPort: {self.port}"
        QMessageBox.information(self, "Info", info)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(QSS)
    login = LoginDialog()
    if login.exec_() == QDialog.Accepted:
        username = login.username
        host = login.host
        port = login.port
        window = ChatClientUI(username, host, port)
        window.show()
        sys.exit(app.exec_()) 