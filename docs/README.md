# BeQuickChat

## Overview
BeQuickChat is a modern, multi-user chat application built with Python and PyQt5, using UDP sockets and a custom protocol for reliable messaging. It features:
- Multi-user chat (general and private)
- Reliable UDP messaging (ACK, retransmission)
- Real-time user list and system messages
- Modern, responsive GUI with chat bubbles and custom icon
- Cross-platform support (Windows, Linux)

## Features
- **Reliable UDP Messaging:** Custom ACK and retransmission logic for message delivery.
- **User List:** Real-time updates of connected users.
- **System Messages:** Join/leave notifications.
- **Private Messaging:** Double-click a user to open a private chat tab.
- **Modern GUI:** Chat bubbles, user list, custom window icon, and responsive design.
- **Customizable:** Easily change the app icon and chat bubble styles.
- **Duplicate Prevention:** Sequence numbers to prevent duplicate messages.

## Installation

### Requirements
- Python 3.8+
- PyQt5 >= 5.15.0
- matplotlib >= 3.5.0 (for performance tests)

### Install dependencies
```bash
pip install -r requirements.txt
```

### File Structure
```
network/
  src/
    client.py
    server.py
    protocol.py
  tests/
    test_functional.py
    test_full.py
    test_performance.py
  docs/
    README.md
    USER_MANUAL.md
  assets/
    close.png
    bequickchat.png
    latency_histogram.png
    latency_per_message.png
    success_pie.png
  reports/
    rapor.docx
  requirements.txt
```

## Usage

### Start the Server
```bash
python src/server.py
```

### Start the Client
```bash
python src/client.py
```
- Enter your username and server address (default: 127.0.0.1:8000).
- Start chatting in the general chat or double-click a user for private chat.

## Customization
- **App Icon:** Change `assets/bequickchat.png` to use your own icon.
- **Tab Close Icon:** Change `assets/close.png` for the tab close button.
- **Chat Bubble Styles:** Edit `src/client.py` in the `ChatBubble` class for custom colors and sizes.

## Protocol Design
- **Message Structure:**  
  Each message contains:  
  `username`, `message`, `seq`, `msg_type` (join, leave, chat, private), `timestamp`
- **Reliability:**  
  - Each message has a unique sequence number.
  - Receiver sends ACK for each message.
  - Sender retransmits if ACK is not received (up to N times).
- **Duplicate Prevention:**  
  - Each client tracks seen sequence numbers per sender.

## Testing
- **Functional Test:**  
  Run `python tests/test_functional.py` to check basic join, chat, and leave functionality.
- **Full Test:**  
  Run `python tests/test_full.py` for a more comprehensive test with two simulated clients.
- **Performance Test:**  
  Run `python tests/test_performance.py` to generate latency and success rate charts (requires matplotlib).

## Performance & Limitations
- **Performance:**  
  Reliable UDP is implemented, but under heavy load or high packet loss, some delays may occur.
- **Limitations:**  
  - No encryption (can be added as an extra feature).
  - Not tested on MacOS (works on Windows/Linux).
  - No file transfer or emoji support.

## Troubleshooting
- If you get `ConnectionResetError`, make sure the server is running and reachable.
- For GUI issues, ensure PyQt5 is installed and Python version is compatible.
- If icons do not appear, check that `assets/bequickchat.png` and `assets/close.png` exist and are valid PNG files.

## Authors
- [Your Name]
- [Your Team Members]

## License
This project is for educational purposes. 