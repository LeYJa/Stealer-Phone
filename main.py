import os
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
import time

# 🔐 Obtenemos las credenciales desde los secrets
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

print("✅ Script iniciado, generando STRING_SESSION...")

with TelegramClient(StringSession(), api_id, api_hash) as client:
    string_session = client.session.save()
    print(f"\n🔐 STRING_SESSION generado:\n{string_session}\n")

# ⏳ Mantener vivo el proceso para que Fly.io no lo mate antes de capturar logs
time.sleep(30)
