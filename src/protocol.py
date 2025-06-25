import json
import time
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

AES_KEY = b'mysecretkey12345'  # 16, 24 veya 32 byte olmalı
AES_IV = b'1234567890abcdef'   # 16 byte IV

def encode_message(username, message, seq=0, msg_type="chat", timestamp=None):
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
    return json.dumps({
        'type': 'user_list',
        'users': user_list
    }).encode('utf-8')

def decode_user_list(data):
    try:
        msg = json.loads(data.decode('utf-8'))
        if msg.get('type') == 'user_list':
            return msg.get('users', [])
        return []
    except Exception:
        return []

def encode_system_message(message, seq=None):
    if seq is None:
        seq = int(time.time() * 1000)  # ms cinsinden timestamp
    return json.dumps({
        'type': 'system',
        'timestamp': time.strftime('%H:%M:%S'),
        'message': message,
        'seq': seq
    }).encode('utf-8')

def decode_system_message(data):
    try:
        msg = json.loads(data.decode('utf-8'))
        if msg.get('type') == 'system':
            return msg.get('timestamp'), msg.get('message'), msg.get('seq')
        return None, None, None
    except Exception:
        return None, None, None

def encode_ack(seq):
    return json.dumps({
        'type': 'ack',
        'seq': seq
    }).encode('utf-8')

def decode_ack(data):
    try:
        msg = json.loads(data.decode('utf-8'))
        if msg.get('type') == 'ack':
            return msg.get('seq')
        return None
    except Exception:
        return None

def encode_private_message(sender, to, message, seq=0, timestamp=None):
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
    cipher = AES.new(AES_KEY, AES.MODE_CBC, AES_IV)
    ct_bytes = cipher.encrypt(pad(raw, AES.block_size))
    return base64.b64encode(ct_bytes)

def decrypt_message(enc: bytes) -> bytes:
    cipher = AES.new(AES_KEY, AES.MODE_CBC, AES_IV)
    ct = base64.b64decode(enc)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    return pt 