"""
Veritabanı paketi — SQLite tabanlı kalıcılık katmanı.
"""

from .schema import init_db
from .queries import (
    authenticate,
    mark_read,
    private_history,
    public_history,
    register_user,
    save_message,
)

__all__ = [
    "init_db",
    "register_user",
    "authenticate",
    "save_message",
    "public_history",
    "private_history",
    "mark_read",
]
