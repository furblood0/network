import socket
import threading
import time
from protocol import encode_message, decode_message, encode_user_list, encode_system_message, encode_ack, decode_ack, decode_private_message

HOST = '0.0.0.0'
PORT = 8000

clients = set()  # (ip, port) tuples
usernames = {}   # addr: username mapping
last_seen_seq = {}  # addr: last seen seq (duplicate prevention)

# =====================
# UDP-based chat server
# =====================

def send_user_list(server):
    """
    Sends the current user list to all connected clients.
    """
    user_list = list(usernames.values())
    data = encode_user_list(user_list)
    for client_addr in clients:
        try:
            server.sendto(data, client_addr)
        except:
            pass

def reliable_send(server, msg, client_addr, seq, max_retries=3, timeout=0.5):
    """
    Provides reliable message sending over UDP (with ACK and retry).
    """
    ack_received = False
    server.settimeout(timeout)
    for _ in range(max_retries):
        server.sendto(msg, client_addr)
        try:
            data, addr = server.recvfrom(4096)
            ack_seq = decode_ack(data)
            if addr == client_addr and ack_seq == seq:
                ack_received = True
                break
        except (socket.timeout, ConnectionResetError, OSError):
            continue
    server.settimeout(None)
    return ack_received

# =====================
# UDP server main loop
# =====================

def main():
    """
    Main UDP server loop. Handles incoming packets and processes them by message type.
    Manages user join/leave, general and private messages, and system messages.
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((HOST, PORT))
    print(f"[SERVER] UDP listening: {HOST}:{PORT}")
    while True:
        try:
            data, addr = server.recvfrom(4096)
        except (ConnectionResetError, OSError):
            continue  # Continue loop on error, don't crash server
        username, message, seq, msg_type, timestamp = decode_message(data)
        # ACK message check
        ack_seq = decode_ack(data)
        if ack_seq is not None:
            continue  # Skip if ACK
        # Private message check
        from_user, to_user, priv_msg, priv_seq, priv_timestamp = decode_private_message(data)
        if from_user and to_user and priv_msg:
            # Send ACK
            ack = encode_ack(priv_seq)
            server.sendto(ack, addr)
            # Find target user
            target_addr = None
            for a, uname in usernames.items():
                if uname == to_user:
                    target_addr = a
                    break
            if target_addr:
                reliable_send(server, data, target_addr, priv_seq)
            continue
        if msg_type == "join":
            clients.add(addr)
            usernames[addr] = username
            last_seen_seq[addr] = set()
            print(f"[+] Joined: {addr} ({username})")
            seq = int(time.time() * 1000)
            sysmsg = encode_system_message(f"{username} joined the chat.", seq=seq)
            for client_addr in clients:
                reliable_send(server, sysmsg, client_addr, seq)
            send_user_list(server)
        elif msg_type == "leave":
            if addr in clients:
                left_username = usernames.get(addr, "?")
                print(f"[-] Left: {addr} ({left_username})")
                clients.remove(addr)
                usernames.pop(addr, None)
                last_seen_seq.pop(addr, None)
                seq = int(time.time() * 1000)
                sysmsg = encode_system_message(f"{left_username} left the chat.", seq=seq)
                for client_addr in clients:
                    reliable_send(server, sysmsg, client_addr, seq)
                send_user_list(server)
        elif msg_type == "chat":
            # Duplicate prevention
            if addr not in last_seen_seq:
                last_seen_seq[addr] = set()
            if seq in last_seen_seq[addr]:
                continue
            last_seen_seq[addr].add(seq)
            # Send ACK
            ack = encode_ack(seq)
            server.sendto(ack, addr)
            print(f"[MSG] {username}: {message}")
            # Relay message to other clients reliably
            for client_addr in clients:
                if client_addr != addr:
                    reliable_send(server, data, client_addr, seq)
            send_user_list(server)

if __name__ == "__main__":
    main() 