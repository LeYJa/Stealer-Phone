import os
import time
from telethon.sync import TelegramClient
from telethon.sessions import StringSession

# Leer los secrets desde Fly.io
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

print("🚀 Iniciando generación de STRING_SESSION...")

with TelegramClient(StringSession(), API_ID, API_HASH) as client:
    string = client.session.save()
    print("\n🔑 STRING_SESSION generado correctamente:\n")
    print(string)
    print("\n✅ Fin del proceso. Puedes copiar la sesión y volver a tu código normal.")

# Mantener el contenedor vivo unos segundos para que Fly lo registre
time.sleep(30)
