"""
Veritabanı sorgu fonksiyonları: kullanıcı, mesaj ve okundu işlemleri.
"""

import hashlib
import os
import sqlite3
from datetime import datetime

from .schema import _conn


# ─────────────────────── Şifre ──────────────────────────────

def _hash(password: str) -> str:
    salt = os.urandom(16)
    key = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100_000)
    return f"{salt.hex()}:{key.hex()}"


def _verify(password: str, stored: str) -> bool:
    try:
        salt_hex, key_hex = stored.split(":")
        key = hashlib.pbkdf2_hmac(
            "sha256", password.encode(), bytes.fromhex(salt_hex), 100_000
        )
        return key.hex() == key_hex
    except Exception:
        return False


# ─────────────────────── Kullanıcı ──────────────────────────

def register_user(username: str, password: str) -> tuple:
    """(başarı: bool, mesaj: str)"""
    username = username.strip()
    if len(username) < 3:
        return False, "Kullanıcı adı en az 3 karakter olmalı"
    if len(password) < 4:
        return False, "Şifre en az 4 karakter olmalı"
    try:
        with _conn() as con:
            con.execute(
                "INSERT INTO users (username, password_hash, created_at) VALUES (?, ?, ?)",
                (username, _hash(password), datetime.now().isoformat()),
            )
        return True, "ok"
    except sqlite3.IntegrityError:
        return False, "Bu kullanıcı adı zaten kullanılıyor"


def authenticate(username: str, password: str) -> tuple:
    """(başarı: bool, mesaj: str)"""
    with _conn() as con:
        row = con.execute(
            "SELECT password_hash FROM users WHERE username = ?", (username.strip(),)
        ).fetchone()
    if row is None:
        return False, "Kullanıcı bulunamadı"
    if _verify(password, row["password_hash"]):
        return True, "ok"
    return False, "Hatalı şifre"


# ─────────────────────── Mesajlar ───────────────────────────

def save_message(
    sender: str, content: str, recipient: str = None, is_private: bool = False
) -> int:
    """Mesajı kaydeder, yeni satır id'sini döndürür."""
    with _conn() as con:
        cur = con.execute(
            "INSERT INTO messages (sender, recipient, content, timestamp, is_private)"
            " VALUES (?, ?, ?, ?, ?)",
            (sender, recipient, content, datetime.now().isoformat(), int(is_private)),
        )
        return cur.lastrowid


def public_history(limit: int = 60) -> list:
    with _conn() as con:
        rows = con.execute(
            "SELECT id, sender, content, timestamp FROM messages"
            " WHERE is_private = 0 ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()
    return [dict(r) for r in reversed(rows)]


def private_history(user1: str, user2: str, limit: int = 60) -> list:
    with _conn() as con:
        rows = con.execute(
            """SELECT id, sender, recipient, content, timestamp FROM messages
               WHERE is_private = 1
                 AND ((sender = ? AND recipient = ?) OR (sender = ? AND recipient = ?))
               ORDER BY id DESC LIMIT ?""",
            (user1, user2, user2, user1, limit),
        ).fetchall()
    return [dict(r) for r in reversed(rows)]


# ─────────────────────── Okundu ─────────────────────────────

def mark_read(message_id: int, reader: str) -> None:
    try:
        with _conn() as con:
            con.execute(
                "INSERT OR IGNORE INTO read_receipts (message_id, reader, read_at)"
                " VALUES (?, ?, ?)",
                (message_id, reader, datetime.now().isoformat()),
            )
    except Exception:
        pass
