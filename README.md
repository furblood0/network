# NetChat

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![PyQt5](https://img.shields.io/badge/PyQt5-5.15+-green.svg)](https://pypi.org/project/PyQt5/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

NetChat, Python ve PyQt5 ile geliştirilmiş TCP tabanlı çok kullanıcılı masaüstü sohbet uygulamasıdır.

## Özellikler

- Kayıt / Giriş sistemi (PBKDF2-SHA256 şifre hash'leme)
- Genel sohbet odası ve özel (bire bir) mesajlaşma
- Mesaj geçmişi (SQLite kalıcılığı)
- Okundu bilgisi (✓ → ✓✓)
- Gerçek zamanlı çevrimiçi kullanıcı listesi
- Katılma / ayrılma sistem bildirimleri
- WhatsApp tarzı koyu tema

## Gereksinimler

- Python 3.12+
- PyQt5 >= 5.15.0

## Kurulum

```bash
git clone https://github.com/furblood0/netchat
cd netchat
pip install -r requirements.txt
```

## Çalıştırma

### 1. Sunucuyu başlatın

```bash
python run_server.py
```

Sunucu `0.0.0.0:9000` adresinde dinlemeye başlar.

### 2. İstemciyi başlatın

```bash
python run_client.py
```

Giriş ekranında sunucu IP adresini, kullanıcı adınızı ve şifrenizi girin.  
Hesabınız yoksa **Hesap Oluştur** butonuyla kayıt olabilirsiniz.

> Aynı ağdaki birden fazla bilgisayarda istemci çalıştırarak test edebilirsiniz.  
> Yerel test için sunucu IP alanını `127.0.0.1` bırakın.

## Proje Yapısı

```
netchat
├── run_client.py          # İstemci giriş noktası
├── run_server.py          # Sunucu giriş noktası
├── requirements.txt
└── src/
    ├── config.py          # Uygulama geneli sabitler (HOST, PORT, DB_PATH…)
    ├── protocol.py        # TCP mesaj çerçeveleme (4-byte uzunluk + JSON)
    ├── database/
    │   ├── schema.py      # Tablo tanımları ve init_db()
    │   └── queries.py     # Kullanıcı, mesaj ve okundu sorguları
    ├── server/
    │   ├── state.py       # Çevrimiçi kullanıcı haritası ve gönderim yardımcıları
    │   ├── handlers.py    # Mesaj tiplerine göre handler fonksiyonları
    │   └── main.py        # asyncio giriş noktası (_handle döngüsü)
    └── client/
        ├── styles.py      # Renk paleti ve QSS stil tanımları
        ├── network.py     # NetworkWorker (arka plan TCP okuma/yazma)
        ├── main.py        # QApplication ve koyu tema kurulumu
        ├── widgets/
        │   ├── bubble.py      # Mesaj balonu
        │   ├── chat_area.py   # Kaydırılabilir mesaj alanı
        │   └── user_row.py    # Sol panel kullanıcı satırı
        └── windows/
            ├── login.py   # Giriş / kayıt ekranı
            └── chat.py    # Ana sohbet penceresi
```

## Protokol

Her TCP mesajı `4 byte büyük-endian uzunluk + UTF-8 JSON payload` şeklinde çerçevelenir.

### İstemci → Sunucu

| Tip                   | Alanlar                        |
|-----------------------|--------------------------------|
| `register`            | `username`, `password`         |
| `login`               | `username`, `password`         |
| `chat`                | `content`                      |
| `private`             | `recipient`, `content`         |
| `get_private_history` | `with`                         |
| `read_receipt`        | `msg_id`, `sender`             |

### Sunucu → İstemci

| Tip               | Alanlar                                          |
|-------------------|--------------------------------------------------|
| `register_result` | `ok`, `reason`                                   |
| `auth_ok`         | `username`                                       |
| `auth_fail`       | `reason`                                         |
| `history`         | `messages`                                       |
| `private_history` | `with`, `messages`                               |
| `chat`            | `msg_id`, `sender`, `content`, `timestamp`       |
| `private`         | `msg_id`, `sender`, `recipient`, `content`, `timestamp` |
| `user_list`       | `users`                                          |
| `system`          | `content`                                        |
| `read_receipt`    | `msg_id`, `reader`                               |

## Geliştiriciler

- **Beyza Nur Selvi** — 222010020057
- **Furkan Fidan** — 212010020002

## Lisans

MIT
