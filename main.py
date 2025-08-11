import os
from telethon.sync import TelegramClient
from telethon.sessions import StringSession

# Cargar la sesión desde las variables de entorno
string_session = os.getenv("STRING_SESSION")

# ✅ Validación y reporte
if not string_session:
    raise ValueError("❌ STRING_SESSION no está definido.")
elif len(string_session) < 275:
    raise ValueError(f"❌ STRING_SESSION demasiado corto ({len(string_session)} caracteres). Se esperan al menos 275.")
else:
    print(f"✅ STRING_SESSION cargado correctamente ({len(string_session)} caracteres).")

# Crear el cliente solo si el string es válido
with TelegramClient(StringSession(string_session), api_id, api_hash) as client:
    print("📡 Cliente conectado correctamente.")
