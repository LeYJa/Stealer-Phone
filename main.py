import os
import asyncio
import logging
from telethon import TelegramClient, events
from telethon.sessions import StringSession

logging.basicConfig(level=logging.INFO)

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
STRING_SESSION = os.getenv("STRING_SESSION")
SOURCE_CHAT = os.getenv("SOURCE_CHAT", "MisicFeed")  # Username o ID
TOPIC_ID = int(os.getenv("TOPIC_ID", "34680"))        # El tema que nos importa

client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)

@client.on(events.NewMessage(chats=SOURCE_CHAT))
async def on_message(event):
    reply_to_topic = getattr(event.message, "reply_to", None)
    if reply_to_topic and reply_to_topic.reply_to_top_id == TOPIC_ID:
        await event.respond("👋 Hello World desde el tema 34680")

async def main():
    await client.start()
    me = await client.get_me()
    logging.info(f"Bot iniciado como @{me.username or me.id}")
    await client.run_until_disconnected()

asyncio.run(main())
