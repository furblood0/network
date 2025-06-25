import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import socket
import time
from protocol import encode_message, decode_message, decode_user_list, encode_ack, decode_ack, encrypt_message, decrypt_message

HOST = '127.0.0.1'
PORT = 8000
USERNAME = 'TestUser'

server_addr = (HOST, PORT)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(2)

print('--- Functionality Test Started ---')

# 1. Send join message
join_msg = encode_message(USERNAME, '', seq=1, msg_type='join')
sock.sendto(encrypt_message(join_msg), server_addr)
print('[TEST] Join message sent.')

# 2. Wait for user list or system message
try:
    data, addr = sock.recvfrom(4096)
    try:
        data = decrypt_message(data)
    except Exception:
        pass
    users = decode_user_list(data)
    if users:
        print(f'[TEST] User list received: {users}')
    else:
        print(f'[TEST] System message or another message received.')
except socket.timeout:
    print('[TEST] User list/system message not received (timeout).')

# 3. Send chat message
chat_msg = encode_message(USERNAME, 'Hello, this is a test message.', seq=2, msg_type='chat', timestamp=time.strftime('%H:%M:%S'))
sock.sendto(encrypt_message(chat_msg), server_addr)
print('[TEST] Chat message sent.')

# 4. Wait for ACK or another message
try:
    data, addr = sock.recvfrom(4096)
    try:
        data = decrypt_message(data)
    except Exception:
        pass
    ack_seq = decode_ack(data)
    if ack_seq is not None:
        print(f'[TEST] ACK received (seq={ack_seq})')
    else:
        username, message, seq, msg_type, timestamp = decode_message(data)
        print(f'[TEST] Message received: {username}: {message}')
except socket.timeout:
    print('[TEST] Message/ACK not received (timeout).')

# 5. Send leave message
leave_msg = encode_message(USERNAME, '', seq=3, msg_type='leave')
sock.sendto(encrypt_message(leave_msg), server_addr)
print('[TEST] Leave message sent.')

sock.close()
print('--- Functionality Test Finished ---')
