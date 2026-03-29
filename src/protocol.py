"""
TCP mesaj çerçeveleme (framing) modülü.

Her mesaj:  [4 byte büyük-endian uzunluk] + [UTF-8 JSON payload]

Bu sayede TCP'nin stream yapısından kaynaklanan bölünmüş/birleşmiş
paket sorunları güvenilir biçimde çözülür.
"""

import json
import logging
import struct

log = logging.getLogger("protocol")

HEADER = 4  # bayt cinsinden başlık boyutu


def encode(data: dict) -> bytes:
    """dict → kabloya gönderilecek bayt dizisi."""
    payload = json.dumps(data, ensure_ascii=False).encode("utf-8")
    return struct.pack(">I", len(payload)) + payload


def decode_buffer(buf: bytes) -> tuple:
    """
    Ham tampon içinden tüm tam mesajları ayıklar.
    Döndürür: (mesaj listesi, kalan tampon)
    """
    messages = []
    while len(buf) >= HEADER:
        length = struct.unpack(">I", buf[:HEADER])[0]
        end = HEADER + length
        if len(buf) < end:
            break
        try:
            messages.append(json.loads(buf[HEADER:end].decode("utf-8")))
        except (json.JSONDecodeError, UnicodeDecodeError):
            log.warning("Geçersiz frame atlandı (uzunluk=%d)", length)
        buf = buf[end:]
    return messages, buf
