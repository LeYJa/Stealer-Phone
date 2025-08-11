import os
from telethon.sync import TelegramClient
from telethon.sessions import StringSession

# Validación de entorno
string_session = os.getenv("STRING_SESSION")
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")

# Validaciones básicas
if not string_session or len(string_session) < 100:
    raise ValueError("❌ STRING_SESSION no válido o demasiado corto.")
if not api_id or not api_hash:
    raise ValueError("❌ API_ID o API_HASH no definidos.")

# Inicializar cliente
with TelegramClient(StringSession(string_session), int(api_id), api_hash) as client:
    me = client.get_me()
    print(f"✅ Sesión iniciada como: {me.username} (ID: {me.id})")
