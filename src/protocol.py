import json
import time
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

# AES encryption key (must be 16, 24, or 32 bytes)
AES_KEY = b'mysecretkey12345'
# AES initialization vector (must be 16 bytes)
AES_IV = b'1234567890abcdef' 

def encode_message(username, message, seq=0, msg_type="chat", timestamp=None):
    """Encode a chat message as JSON bytes for sending over the network."""
    if timestamp is None:
        timestamp = time.strftime('%H:%M:%S')
    return json.dumps({
        'username': username,
        'message': message,
        'seq': seq,
        'type': msg_type,
        'timestamp': timestamp
    }).encode('utf-8')

def decode_message(data):
    """Decode received JSON bytes into message fields (username, message, etc)."""
    try:
        msg = json.loads(data.decode('utf-8'))
        return (
            msg.get('username'),
            msg.get('message'),
            msg.get('seq', 0),
            msg.get('type', 'chat'),
            msg.get('timestamp', None)
        )
    except Exception:
        return None, None, 0, 'chat', None

def encode_user_list(user_list):
    """Encode the user list as JSON bytes for transmission."""
    return json.dumps({
        'type': 'user_list',
        'users': user_list
    }).encode('utf-8')

def decode_user_list(data):
    """Decode received JSON bytes into a list of users."""
    try:
        msg = json.loads(data.decode('utf-8'))
        if msg.get('type') == 'user_list':
            return msg.get('users', [])
        return []
    except Exception:
        return []

def encode_system_message(message, seq=None):
    """Encode a system message (e.g., notifications) as JSON bytes."""
    if seq is None:
        seq = int(time.time() * 1000)  # ms cinsinden timestamp
    return json.dumps({
        'type': 'system',
        'timestamp': time.strftime('%H:%M:%S'),
        'message': message,
        'seq': seq
    }).encode('utf-8')

def decode_system_message(data):
    """Decode received JSON bytes into a system message and its fields."""
    try:
        msg = json.loads(data.decode('utf-8'))
        if msg.get('type') == 'system':
            return msg.get('timestamp'), msg.get('message'), msg.get('seq')
        return None, None, None
    except Exception:
        return None, None, None

def encode_ack(seq):
    """Encode an ACK (acknowledgment) message as JSON bytes."""
    return json.dumps({
        'type': 'ack',
        'seq': seq
    }).encode('utf-8')

def decode_ack(data):
    """Decode received JSON bytes to extract the ACK sequence number."""
    try:
        msg = json.loads(data.decode('utf-8'))
        if msg.get('type') == 'ack':
            return msg.get('seq')
        return None
    except Exception:
        return None

def encode_private_message(sender, to, message, seq=0, timestamp=None):
    """Encode a private (direct) message as JSON bytes."""
    if timestamp is None:
        timestamp = time.strftime('%H:%M:%S')
    return json.dumps({
        'type': 'private',
        'from': sender,
        'to': to,
        'message': message,
        'seq': seq,
        'timestamp': timestamp
    }).encode('utf-8')

def decode_private_message(data):
    """Decode received JSON bytes into private message fields."""
    try:
        msg = json.loads(data.decode('utf-8'))
        if msg.get('type') == 'private':
            return (
                msg.get('from'),
                msg.get('to'),
                msg.get('message'),
                msg.get('seq', 0),
                msg.get('timestamp', None)
            )
        return None, None, None, 0, None
    except Exception:
        return None, None, None, 0, None

def encrypt_message(raw: bytes) -> bytes:
    """Encrypt a message using AES-CBC and return base64-encoded bytes."""
    cipher = AES.new(AES_KEY, AES.MODE_CBC, AES_IV)
    ct_bytes = cipher.encrypt(pad(raw, AES.block_size))
    return base64.b64encode(ct_bytes)

def decrypt_message(enc: bytes) -> bytes:
    """Decrypt a base64-encoded AES-CBC encrypted message."""
    cipher = AES.new(AES_KEY, AES.MODE_CBC, AES_IV)
    ct = base64.b64decode(enc)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    return pt 