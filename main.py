from telethon.sync import TelegramClient
from telethon.sessions import StringSession
import os

# Carga de credenciales desde los secretos
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
string_session = os.getenv("STRING_SESSION")
chat_id = os.getenv("CHAT_ID")         # Username o ID del grupo, ej: "@MiGrupo"
topic_id = int(os.getenv("TOPIC_ID"))  # ID del tema donde queremos publicar

# Inicializar y enviar mensaje dentro del topic
with TelegramClient(StringSession(string_session), api_id, api_hash) as client:
    client.send_message(chat_id, "Hello World 👋", reply_to=topic_id)
