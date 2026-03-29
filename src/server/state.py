"""
Sunucu durumu: çevrimiçi kullanıcı haritası ve gönderim yardımcıları.
"""

import asyncio
import logging
from typing import Optional

from protocol import encode

log = logging.getLogger("server.state")

_online: dict[str, asyncio.StreamWriter] = {}


# ─────────────────────── Oturum yönetimi ────────────────────

def add_client(username: str, writer: asyncio.StreamWriter) -> None:
    _online[username] = writer


def remove_client(username: str) -> None:
    _online.pop(username, None)


def get_writer(username: str) -> Optional[asyncio.StreamWriter]:
    return _online.get(username)


def is_online(username: str) -> bool:
    return username in _online


def get_all_usernames() -> list[str]:
    return list(_online.keys())


# ─────────────────────── Gönderim yardımcıları ──────────────

async def send(writer: asyncio.StreamWriter, data: dict) -> None:
    try:
        writer.write(encode(data))
        await writer.drain()
    except Exception:
        pass


async def broadcast(data: dict, exclude: str = None) -> None:
    for uname, w in list(_online.items()):
        if uname != exclude:
            await send(w, data)


async def push_user_list() -> None:
    msg = {"type": "user_list", "users": get_all_usernames()}
    for w in list(_online.values()):
        await send(w, msg)
