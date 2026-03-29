"""
Veritabanı şeması: bağlantı yardımcısı ve tablo oluşturma.
"""

import sqlite3

from config import DB_PATH


def _conn() -> sqlite3.Connection:
    con = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA journal_mode=WAL")
    return con


def init_db() -> None:
    """Veritabanını ve tabloları oluşturur (yoksa)."""
    with _conn() as con:
        con.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                username      TEXT    UNIQUE NOT NULL,
                password_hash TEXT    NOT NULL,
                created_at    TEXT    NOT NULL
            );

            CREATE TABLE IF NOT EXISTS messages (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                sender     TEXT    NOT NULL,
                recipient  TEXT,
                content    TEXT    NOT NULL,
                timestamp  TEXT    NOT NULL,
                is_private INTEGER NOT NULL DEFAULT 0
            );

            CREATE TABLE IF NOT EXISTS read_receipts (
                message_id INTEGER NOT NULL,
                reader     TEXT    NOT NULL,
                read_at    TEXT    NOT NULL,
                PRIMARY KEY (message_id, reader)
            );
        """)
