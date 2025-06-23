import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import socket
import time
from protocol import encode_message, decode_message, decode_user_list, encode_ack, decode_ack, decode_system_message

HOST = '127.0.0.1'
PORT = 8000
ADDR = (HOST, PORT)
USERNAME = 'TestUser1'

print('--- Full Single-Client Functionality Test Started ---')

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(2)

# 1. Join
join_msg = encode_message(USERNAME, '', seq=1, msg_type='join')
sock.sendto(join_msg, ADDR)
print('[TEST] Join message sent.')

# 2. Wait for user list or system message
try:
    for _ in range(3):
        data, addr = sock.recvfrom(4096)
        users = decode_user_list(data)
        if users:
            print(f'[TEST] User list received: {users}')
            break
        timestamp, sysmsg, sysseq = decode_system_message(data)
        if sysmsg:
            print(f'[TEST] System message received: {sysmsg}')
            break
    else:
        print('[TEST] No user list or system message received.')
except socket.timeout:
    print('[TEST] User list/system message not received (timeout).')

# 3. Send public message
chat_msg = encode_message(USERNAME, 'Hello, this is a test message.', seq=2, msg_type='chat', timestamp=time.strftime('%H:%M:%S'))
sock.sendto(chat_msg, ADDR)
print('[TEST] Public chat message sent.')

# 4. Wait for ACK or message (improved loop)
ack_received = False
start_time = time.time()
while time.time() - start_time < 2.0:
    try:
        data, addr = sock.recvfrom(4096)
        ack_seq = decode_ack(data)
        if ack_seq is not None:
            print(f'[TEST] ACK received (seq={ack_seq})')
            ack_received = True
            break
        username, message, seq, msg_type, timestamp = decode_message(data)
        if msg_type == 'chat' and username:
            print(f'[TEST] Chat message received: {username}: {message}')
    except socket.timeout:
        break
if not ack_received:
    print('[TEST] ACK not received.')

# 5. Leave
leave_msg = encode_message(USERNAME, '', seq=3, msg_type='leave')
sock.sendto(leave_msg, ADDR)
print('[TEST] Leave message sent.')

sock.close()
print('--- Full Single-Client Functionality Test Finished ---') 