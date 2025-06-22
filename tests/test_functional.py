import socket
import time
from protocol import encode_message, decode_message, decode_user_list, encode_ack, decode_ack

HOST = '127.0.0.1'
PORT = 8000
USERNAME = 'TestUser'

server_addr = (HOST, PORT)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(2)

print('--- Fonksiyonellik Testi Başladı ---')

# 1. Katılma mesajı gönder
join_msg = encode_message(USERNAME, '', seq=1, msg_type='join')
sock.sendto(join_msg, server_addr)
print('[TEST] Katılma mesajı gönderildi.')

# 2. Kullanıcı listesi veya sistem mesajı bekle
try:
    data, addr = sock.recvfrom(4096)
    users = decode_user_list(data)
    if users:
        print(f'[TEST] Kullanıcı listesi alındı: {users}')
    else:
        print(f'[TEST] Sistem mesajı veya başka bir mesaj alındı.')
except socket.timeout:
    print('[TEST] Kullanıcı listesi/sistem mesajı alınamadı (timeout).')

# 3. Sohbete mesaj gönder
chat_msg = encode_message(USERNAME, 'Merhaba, bu bir test mesajıdır.', seq=2, msg_type='chat', timestamp=time.strftime('%H:%M:%S'))
sock.sendto(chat_msg, server_addr)
print('[TEST] Sohbet mesajı gönderildi.')

# 4. ACK veya başka mesaj bekle
try:
    data, addr = sock.recvfrom(4096)
    ack_seq = decode_ack(data)
    if ack_seq is not None:
        print(f'[TEST] ACK alındı (seq={ack_seq})')
    else:
        username, message, seq, msg_type, timestamp = decode_message(data)
        print(f'[TEST] Mesaj alındı: {username}: {message}')
except socket.timeout:
    print('[TEST] Mesaj/ACK alınamadı (timeout).')

# 5. Ayrılma mesajı gönder
leave_msg = encode_message(USERNAME, '', seq=3, msg_type='leave')
sock.sendto(leave_msg, server_addr)
print('[TEST] Ayrılma mesajı gönderildi.')

sock.close()
print('--- Fonksiyonellik Testi Bitti ---')
