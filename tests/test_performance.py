import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import socket
import time
import threading
import matplotlib.pyplot as plt
from protocol import encode_message, decode_ack, encrypt_message, decrypt_message

HOST = '127.0.0.1'
PORT = 8000
ADDR = (HOST, PORT)

USERNAME = 'PerfTestUser'
N = 200  # Gönderilecek mesaj sayısı
CONCURRENCY = 1  # Aynı anda kaç istemci/thread test edecek

delays = []
success_count = 0
fail_count = 0
lock = threading.Lock()

def run_test(client_id):
    global success_count, fail_count
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(2)
    join_msg = encode_message(f"{USERNAME}{client_id}", '', seq=0, msg_type='join')
    sock.sendto(encrypt_message(join_msg), ADDR)
    time.sleep(0.2)

    for i in range(1, N+1):
        msg = f"Test message {i} from {client_id}"
        seq = i
        data = encode_message(f"{USERNAME}{client_id}", msg, seq=seq, msg_type='chat', timestamp=time.strftime('%H:%M:%S'))
        sock.sendto(encrypt_message(data), ADDR)
        start = time.time()
        try:
            while True:
                ack_data, _ = sock.recvfrom(4096)
                try:
                    ack_data = decrypt_message(ack_data)
                except Exception:
                    continue
                ack_seq = decode_ack(ack_data)
                if ack_seq == seq:
                    break
            end = time.time()
            delay = (end - start) * 1000  # ms
            with lock:
                delays.append(delay)
                success_count += 1
            print(f"[{client_id}][{i}] ACK received, delay: {delay:.2f} ms")
        except socket.timeout:
            with lock:
                fail_count += 1
            print(f"[{client_id}][{i}] ACK not received (timeout)")

    leave_msg = encode_message(f"{USERNAME}{client_id}", '', seq=N+1, msg_type='leave')
    sock.sendto(encrypt_message(leave_msg), ADDR)
    sock.close()

if __name__ == "__main__":
    print('--- Performance Test Started ---')
    threads = []
    for c in range(CONCURRENCY):
        t = threading.Thread(target=run_test, args=(c,))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()

    print(f"\nTotal messages: {N * CONCURRENCY}")
    print(f"Successful: {success_count}")
    print(f"Timeouts: {fail_count}")
    if delays:
        print(f"Average delay: {sum(delays)/len(delays):.2f} ms")
        print(f"Minimum delay: {min(delays):.2f} ms")
        print(f"Maximum delay: {max(delays):.2f} ms")

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
        success = success_count
        fail = fail_count
        plt.figure(figsize=(5,5))
        plt.pie([success, fail], labels=['Successful', 'Timeout'], autopct='%1.1f%%', colors=['#4CAF50', '#F44336'])
        plt.title('Successful Message Rate')
        plt.tight_layout()
        plt.savefig('success_pie.png')
        plt.show()
    else:
        print("No ACKs received!")

    print('--- Performance Test Finished ---') 