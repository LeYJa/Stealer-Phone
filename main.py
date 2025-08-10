from telethon import TelegramClient, events
import re
import os

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION_NAME = "bot_session"

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

# Regex para detectar números (móviles, fijos…)
PHONE_REGEX = r'\b(?:\+34)?(?:6\d{8}|7\d{8}|9\d{8})\b'

@client.on(events.NewMessage(chats='tu_grupo_de_telegram'))  # Reemplaza con el ID o username del grupo
async def handler(event):
    matches = re.findall(PHONE_REGEX, event.raw_text)
    for number in matches:
        if not number.startswith('+34'):
            number = '+34' + number
        await client.send_message('@TrueCaller1Bot', number)
        response = await client.get_messages('@TrueCaller1Bot', limit=1)
        await client.send_message('tu_grupo_de_telegram', f'[Estafa detectada] {response.message}', reply_to=event.id)

client.start()
client.run_until_disconnected()
