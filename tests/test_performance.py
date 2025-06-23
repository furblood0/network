import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import socket
import time
from protocol import encode_message, decode_ack
import matplotlib.pyplot as plt

HOST = '127.0.0.1'
PORT = 8000
ADDR = (HOST, PORT)
USERNAME = 'PerfTestUser'

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(2)

N = 100  # Number of messages to send
delays = []

print('--- Performance Test Started ---')

# Join message
join_msg = encode_message(USERNAME, '', seq=0, msg_type='join')
sock.sendto(join_msg, ADDR)
time.sleep(0.5)

for i in range(1, N+1):
    msg = f"Test message {i}"
    seq = i
    data = encode_message(USERNAME, msg, seq=seq, msg_type='chat', timestamp=time.strftime('%H:%M:%S'))
    start = time.time()
    sock.sendto(data, ADDR)
    try:
        while True:
            ack_data, _ = sock.recvfrom(4096)
            ack_seq = decode_ack(ack_data)
            if ack_seq == seq:
                break
        end = time.time()
        delay = (end - start) * 1000  # ms
        delays.append(delay)
        print(f"[{i}] ACK received, delay: {delay:.2f} ms")
    except socket.timeout:
        print(f"[{i}] ACK not received (timeout)")

# Leave message
leave_msg = encode_message(USERNAME, '', seq=N+1, msg_type='leave')
sock.sendto(leave_msg, ADDR)
sock.close()

if delays:
    print(f"\nAverage delay: {sum(delays)/len(delays):.2f} ms")
    print(f"Minimum delay: {min(delays):.2f} ms")
    print(f"Maximum delay: {max(delays):.2f} ms")
    print(f"Successful message rate: {len(delays)}/{N}")

    # 1. Latency per message graph
    plt.figure(figsize=(10,5))
    plt.plot(range(1, len(delays)+1), delays, marker='o')
    plt.xlabel('Message Number')
    plt.ylabel('Delay (ms)')
    plt.title('Latency per Message')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('latency_per_message.png')
    plt.show()

    # 2. Delay histogram
    plt.figure(figsize=(8,4))
    plt.hist(delays, bins=20, color='skyblue', edgecolor='black')
    plt.xlabel('Delay (ms)')
    plt.ylabel('Number of Messages')
    plt.title('Delay Distribution Histogram')
    plt.tight_layout()
    plt.savefig('latency_histogram.png')
    plt.show()

    # 3. Success rate pie chart
    success = len(delays)
    fail = N - success
    plt.figure(figsize=(5,5))
    plt.pie([success, fail], labels=['Successful', 'Timeout'], autopct='%1.1f%%', colors=['#4CAF50', '#F44336'])
    plt.title('Successful Message Rate')
    plt.tight_layout()
    plt.savefig('success_pie.png')
    plt.show()
else:
    print("No ACKs received!")

print('--- Performance Test Finished ---') 