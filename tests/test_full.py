import sys
import os
import socket
import time
import threading
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from protocol import encode_message, decode_message, decode_user_list, encode_ack, decode_ack, decode_system_message, encrypt_message, decrypt_message

HOST = '127.0.0.1'
PORT = 8000
ADDR = (HOST, PORT)
USERNAMES = ['TestUser1', 'TestUser2']

print('--- Multi-Client Full Functionality Test Started ---')

results = []

def client_test(username, seq_offset=0):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(2)
    join_msg = encode_message(username, '', seq=1+seq_offset, msg_type='join')
    sock.sendto(encrypt_message(join_msg), ADDR)
    print(f'[{username}] Join message sent.')

    # Wait for user list or system message
    try:
        for _ in range(3):
            data, addr = sock.recvfrom(4096)
            try:
                data = decrypt_message(data)
            except Exception:
                pass
            users = decode_user_list(data)
            if users:
                print(f'[{username}] User list received: {users}')
                break
            timestamp, sysmsg, sysseq = decode_system_message(data)
            if sysmsg:
                print(f'[{username}] System message received: {sysmsg}')
                break
        else:
            print(f'[{username}] No user list or system message received.')
    except socket.timeout:
        print(f'[{username}] User list/system message not received (timeout).')

    # Send public message
    chat_msg = encode_message(username, f'Hello from {username}', seq=2+seq_offset, msg_type='chat', timestamp=time.strftime('%H:%M:%S'))
    sock.sendto(encrypt_message(chat_msg), ADDR)
    print(f'[{username}] Public chat message sent.')

    # Wait for ACK or message
    ack_received = False
    start_time = time.time()
    while time.time() - start_time < 2.0:
        try:
            data, addr = sock.recvfrom(4096)
            try:
                data = decrypt_message(data)
            except Exception:
                pass
            ack_seq = decode_ack(data)
            if ack_seq == 2+seq_offset:
                print(f'[{username}] ACK received (seq={ack_seq})')
                ack_received = True
                break
            uname, message, seq, msg_type, timestamp = decode_message(data)
            if msg_type == 'chat' and uname:
                print(f'[{username}] Chat message received: {uname}: {message}')
        except socket.timeout:
            break
    if not ack_received:
        print(f'[{username}] ACK not received.')
    results.append((username, ack_received))

    # Leave
    leave_msg = encode_message(username, '', seq=3+seq_offset, msg_type='leave')
    sock.sendto(encrypt_message(leave_msg), ADDR)
    print(f'[{username}] Leave message sent.')
    sock.close()

threads = []
for i, uname in enumerate(USERNAMES):
    t = threading.Thread(target=client_test, args=(uname, i*10))
    t.start()
    threads.append(t)
for t in threads:
    t.join()

print('\n--- Multi-Client Full Functionality Test Results ---')
for username, ack in results:
    print(f'{username}: ACK received? {"YES" if ack else "NO"}')
print('--- Test Finished ---') 