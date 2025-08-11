import os
from telethon.sync import TelegramClient
from telethon.sessions import StringSession

# Accede desde variables de entorno
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

with TelegramClient(StringSession(), api_id, api_hash) as client:
    print("🔑 STRING_SESSION generado correctamente:\n")
    print(client.session.save())
