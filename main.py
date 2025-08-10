import os
import re
import asyncio
import logging
from aiohttp import web

from telethon import events
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.types import InputReplyToForumTopic

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

# Config
API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
STRING_SESSION = os.environ.get("STRING_SESSION")
SOURCE_CHAT = os.environ.get("SOURCE_CHAT")  # ej: -1001234567890 o "MisicFeed"
TARGET_CHAT = os.environ.get("TARGET_CHAT", SOURCE_CHAT)
TRUECALLER_BOT = os.environ.get("TRUECALLER_BOT", "TrueCaller1Bot")
TOPIC_ID = os.environ.get("TOPIC_ID")
TOPIC_ID = int(TOPIC_ID) if TOPIC_ID else None

# Puerto para healthcheck HTTP (Fly)
PORT = int(os.environ.get("PORT", "8080"))

# Regex teléfonos
PHONE_PATTERN = re.compile(r"\+?\d[\d\s\-\.\(\)]{7,16}\d")

RECENT_CACHE = {}
CACHE_TTL = 60 * 30  # 30 min

def normalize_spanish(num_raw: str):
    digits = "".join(c for c in num_raw if c.isdigit())
    if len(digits) < 9:
        return None
    if len(digits) == 9:
        return f"+34{digits}"
    if len(digits) == 11 and digits.startswith("34"):
        return f"+{digits}"
    if num_raw.strip().startswith("+"):
        return f"+{digits}"
    return None

async def query_truecaller(client: TelegramClient, number: str, timeout: int = 45):
    async with client.conversation(TRUECALLER_BOT, timeout=timeout) as conv:
        await conv.send_message(number)
        reply = await conv.get_response()
        text = (reply.message or getattr(reply, "text", "") or "").strip()
        return text or "Sin contenido de texto."

async def send_to_topic(client: TelegramClient, chat, topic_id: int, text: str):
    await client.send_message(chat, text, reply_to=InputReplyToForumTopic(topic_id=topic_id))

def purge_cache(now: float):
    stale = [k for k, t in RECENT_CACHE.items() if now - t > CACHE_TTL]
    for k in stale:
        RECENT_CACHE.pop(k, None)

async def start_userbot():
    if not (API_ID and API_HASH and STRING_SESSION and SOURCE_CHAT):
        logging.warning("Faltan variables de entorno para Telethon (API_ID, API_HASH, STRING_SESSION, SOURCE_CHAT). Solo se iniciará el servidor HTTP.")
        while True:
            await asyncio.sleep(3600)

    api_id = int(API_ID)
    client = TelegramClient(StringSession(STRING_SESSION), api_id, API_HASH)
    await client.start()
    me = await client.get_me()
    logging.info(f"Userbot iniciado como @{me.username or me.id}")

    if TOPIC_ID is None:
        logging.warning("TOPIC_ID no está definido. Si necesitas enviar a un tema específico, define TOPIC_ID en secrets.")

    @client.on(events.NewMessage(chats=SOURCE_CHAT))
    async def handler(event):
        try:
            text = event.raw_text or ""
            matches = PHONE_PATTERN.findall(text)
            now = event.date.timestamp()
            purge_cache(now)

            normalized = []
            for m in matches:
                n = normalize_spanish(m)
                if not n:
                    continue
                if n in RECENT_CACHE and now - RECENT_CACHE[n] < 10:
                    continue
                RECENT_CACHE[n] = now
                normalized.append(n)

            if not normalized:
                return

            for number in set(normalized):
                logging.info(f"Consultando {number} en @{TRUECALLER_BOT}…")
                try:
                    info = await query_truecaller(client, number)
                except Exception as e:
                    logging.exception(f"Error consultando {number}: {e}")
                    continue

                msg = (
                    f"🔎 Resultado Truecaller para {number}\n"
                    f"{info}"
                )
                target_chat = TARGET_CHAT or event.chat_id

                if TOPIC_ID:
                    try:
                        await send_to_topic(client, target_chat, TOPIC_ID, msg)
                    except Exception as e:
                        logging.exception(f"No se pudo enviar al tema {TOPIC_ID}: {e}. Envío al chat sin tema.")
                        await client.send_message(target_chat, msg)
                else:
                    await client.send_message(target_chat, msg)

        except Exception as e:
            logging.exception(f"Fallo en handler: {e}")

    logging.info("Escuchando mensajes…")
    await client.run_until_disconnected()

async def start_http():
    app = web.Application()
    async def ok(_):
        return web.Response(text="ok")
    app.router.add_get("/", ok)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()
    logging.info(f"HTTP listo en :{PORT} para healthcheck")
    while True:
        await asyncio.sleep(3600)

async def main():
    await asyncio.gather(start_http(), start_userbot())

if __name__ == "__main__":
    asyncio.run(main())
