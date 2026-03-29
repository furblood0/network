"""
Mesaj tiplerine göre sunucu handler fonksiyonları.
"""

import logging
from datetime import datetime
from typing import Optional

from database import (
    authenticate,
    mark_read,
    private_history,
    public_history,
    register_user,
    save_message,
)
from .state import (
    add_client,
    broadcast,
    get_writer,
    is_online,
    push_user_list,
    send,
)

log = logging.getLogger("server.handlers")


async def handle_register(writer, msg: dict) -> None:
    ok, reason = register_user(msg.get("username", ""), msg.get("password", ""))
    await send(writer, {"type": "register_result", "ok": ok, "reason": reason})


async def handle_login(writer, msg: dict) -> Optional[str]:
    """Giriş başarılıysa kullanıcı adını, aksi hâlde None döndürür."""
    uname = msg.get("username", "").strip()
    ok, reason = authenticate(uname, msg.get("password", ""))

    if not ok:
        await send(writer, {"type": "auth_fail", "reason": reason})
        return None

    if is_online(uname):
        await send(writer, {"type": "auth_fail", "reason": "Bu kullanıcı zaten giriş yapmış"})
        return None

    add_client(uname, writer)
    log.info("%s giriş yaptı", uname)

    await send(writer, {"type": "auth_ok", "username": uname})
    await send(writer, {"type": "history", "messages": public_history()})
    await push_user_list()
    await broadcast(
        {"type": "system", "content": f"{uname} sohbete katıldı"},
        exclude=uname,
    )
    return uname


async def handle_chat(username: str, msg: dict) -> None:
    content = msg.get("content", "").strip()
    if not content:
        return
    mid = save_message(username, content)
    await broadcast({
        "type": "chat",
        "msg_id": mid,
        "sender": username,
        "content": content,
        "timestamp": datetime.now().isoformat(),
    })


async def handle_private(writer, username: str, msg: dict) -> None:
    recipient = msg.get("recipient", "").strip()
    content = msg.get("content", "").strip()
    if not recipient or not content:
        return
    mid = save_message(username, content, recipient=recipient, is_private=True)
    out = {
        "type": "private",
        "msg_id": mid,
        "sender": username,
        "recipient": recipient,
        "content": content,
        "timestamp": datetime.now().isoformat(),
    }
    await send(writer, out)
    if recipient != username:
        rw = get_writer(recipient)
        if rw:
            await send(rw, out)


async def handle_get_private_history(writer, username: str, msg: dict) -> None:
    other = msg.get("with", "").strip()
    if other:
        await send(writer, {
            "type": "private_history",
            "with": other,
            "messages": private_history(username, other),
        })


async def handle_read_receipt(username: str, msg: dict) -> None:
    mid = msg.get("msg_id")
    sender = msg.get("sender", "")
    if mid and sender:
        mark_read(mid, username)
        if sender != username:
            sw = get_writer(sender)
            if sw:
                await send(sw, {
                    "type": "read_receipt",
                    "msg_id": mid,
                    "reader": username,
                })
