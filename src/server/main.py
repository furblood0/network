"""
NetChat — asyncio TCP Sunucu giriş noktası.

Desteklenen mesaj tipleri (client → server):
  register            {username, password}
  login               {username, password}
  chat                {content}
  private             {recipient, content}
  get_private_history {with}
  read_receipt        {msg_id, sender}

Gönderilen mesaj tipleri (server → client):
  register_result     {ok, reason}
  auth_ok             {username}
  auth_fail           {reason}
  history             {messages}
  private_history     {with, messages}
  chat                {msg_id, sender, content, timestamp}
  private             {msg_id, sender, recipient, content, timestamp}
  user_list           {users}
  system              {content}
  read_receipt        {msg_id, reader}
"""

import asyncio
import logging

from config import HOST, PORT
from database import init_db
from protocol import decode_buffer
from .handlers import (
    handle_chat,
    handle_get_private_history,
    handle_login,
    handle_private,
    handle_read_receipt,
    handle_register,
)
from .state import broadcast, push_user_list, remove_client

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-7s  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("server.main")


async def _handle(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    addr = writer.get_extra_info("peername")
    log.info("Bağlandı: %s", addr)
    username: str | None = None
    buf = b""

    try:
        while True:
            chunk = await reader.read(8192)
            if not chunk:
                break

            buf += chunk
            messages, buf = decode_buffer(buf)

            for msg in messages:
                t = msg.get("type")

                if t == "register":
                    await handle_register(writer, msg)

                elif t == "login" and username is None:
                    username = await handle_login(writer, msg)

                elif t == "chat" and username:
                    await handle_chat(username, msg)

                elif t == "private" and username:
                    await handle_private(writer, username, msg)

                elif t == "get_private_history" and username:
                    await handle_get_private_history(writer, username, msg)

                elif t == "read_receipt" and username:
                    await handle_read_receipt(username, msg)

    except asyncio.CancelledError:
        pass
    except Exception as exc:
        log.error("Hata (%s): %s", username or addr, exc)
    finally:
        if username:
            remove_client(username)
            log.info("%s ayrıldı", username)
            await broadcast({"type": "system", "content": f"{username} ayrıldı"})
            await push_user_list()
        try:
            writer.close()
            await writer.wait_closed()
        except Exception:
            pass


async def main() -> None:
    init_db()
    server = await asyncio.start_server(_handle, HOST, PORT)
    addrs = ", ".join(str(s.getsockname()) for s in server.sockets)
    log.info("NetChat sunucusu dinliyor → %s", addrs)
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
