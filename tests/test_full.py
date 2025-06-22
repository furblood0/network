import socket
import time
from protocol import encode_message, decode_message, decode_user_list, encode_ack, decode_ack, encode_private_message, decode_private_message, decode_system_message

HOST = '127.0.0.1'
PORT = 8000
ADDR = (HOST, PORT)

USER1 = 'TestUser1'
USER2 = 'TestUser2'

print('--- Kapsamlı Fonksiyonellik Testi Başladı ---')

# İki istemci başlat
sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock1.settimeout(2)
sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock2.settimeout(2)

# 1. Her iki istemci katılsın
join1 = encode_message(USER1, '', seq=1, msg_type='join')
join2 = encode_message(USER2, '', seq=1, msg_type='join')
sock1.sendto(join1, ADDR)
sock2.sendto(join2, ADDR)
print('[TEST] Her iki istemci katıldı.')

time.sleep(0.5)

# 2. Her iki istemci kullanıcı listesi ve sistem mesajı alsın
def wait_for_userlist(sock, user):
    try:
        for _ in range(3):
            data, addr = sock.recvfrom(4096)
            users = decode_user_list(data)
            if users:
                print(f'[TEST] {user} kullanıcı listesi: {users}')
                return users
            timestamp, sysmsg, sysseq = decode_system_message(data)
            if sysmsg:
                print(f'[TEST] {user} sistem mesajı: {sysmsg}')
    except socket.timeout:
        print(f'[TEST] {user} kullanıcı listesi/sistem mesajı alınamadı (timeout).')

wait_for_userlist(sock1, USER1)
wait_for_userlist(sock2, USER2)

# 3. Genel sohbete mesaj gönder (User1)
chat1 = encode_message(USER1, 'Merhaba, bu genel bir mesajdır.', seq=2, msg_type='chat', timestamp=time.strftime('%H:%M:%S'))
sock1.sendto(chat1, ADDR)
print('[TEST] User1 genel mesaj gönderdi.')

# 4. User2 genel mesajı alsın ve ACK göndersin
def wait_for_chat(sock, user):
    try:
        for _ in range(3):
            data, addr = sock.recvfrom(4096)
            username, message, seq, msg_type, timestamp = decode_message(data)
            if msg_type == 'chat' and username:
                print(f'[TEST] {user} genel mesaj aldı: {username}: {message}')
                return True
            ack_seq = decode_ack(data)
            if ack_seq is not None:
                print(f'[TEST] {user} ACK aldı (seq={ack_seq})')
    except socket.timeout:
        print(f'[TEST] {user} genel mesaj/ACK alınamadı (timeout).')

wait_for_chat(sock2, USER2)

# 5. Duplicate engelleme testi (aynı mesajı tekrar gönder)
sock1.sendto(chat1, ADDR)
print('[TEST] User1 duplicate genel mesaj gönderdi.')
wait_for_chat(sock2, USER2)  # User2 duplicate mesajı almamalı (ya da ignore etmeli)

# 6. Özel mesaj gönder (User1 -> User2)
priv_seq = 3
priv_msg = encode_private_message(USER1, USER2, 'Bu bir özel mesajdır.', seq=priv_seq, timestamp=time.strftime('%H:%M:%S'))
sock1.sendto(priv_msg, ADDR)
print('[TEST] User1, User2 ye özel mesaj gönderdi.')

def wait_for_private(sock, user):
    try:
        for _ in range(3):
            data, addr = sock.recvfrom(4096)
            from_user, to_user, priv_msg, priv_seq, priv_timestamp = decode_private_message(data)
            if from_user and to_user and priv_msg:
                print(f'[TEST] {user} özel mesaj aldı: {from_user} -> {to_user}: {priv_msg}')
                return True
            ack_seq = decode_ack(data)
            if ack_seq is not None:
                print(f'[TEST] {user} özel mesaj ACK aldı (seq={ack_seq})')
    except socket.timeout:
        print(f'[TEST] {user} özel mesaj/ACK alınamadı (timeout).')

wait_for_private(sock2, USER2)

# 7. User2 genel mesaj göndersin
chat2 = encode_message(USER2, 'User2 den selamlar!', seq=4, msg_type='chat', timestamp=time.strftime('%H:%M:%S'))
sock2.sendto(chat2, ADDR)
print('[TEST] User2 genel mesaj gönderdi.')
wait_for_chat(sock1, USER1)

# 8. User1 ve User2 ayrılır
leave1 = encode_message(USER1, '', seq=5, msg_type='leave')
leave2 = encode_message(USER2, '', seq=5, msg_type='leave')
sock1.sendto(leave1, ADDR)
sock2.sendto(leave2, ADDR)
print('[TEST] Her iki istemci ayrılma mesajı gönderdi.')

wait_for_userlist(sock1, USER1)
wait_for_userlist(sock2, USER2)

sock1.close()
sock2.close()
print('--- Kapsamlı Fonksiyonellik Testi Bitti ---') 