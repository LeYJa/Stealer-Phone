import os
import logging
from pyrogram import Client
from pyrogram.errors import SessionPasswordNeeded, ApiIdInvalid, PhoneNumberInvalid

# Configura el logger para Fly.io
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Carga de variables de entorno
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
string_session = os.getenv("STRING_SESSION")

# Validación inicial
if not string_session or len(string_session) < 275:
    logging.error("❌ STRING_SESSION inválido o incompleto. Verifica tu sesión.")
    exit(1)

if not api_id or not api_hash:
    logging.error("❌ API_ID o API_HASH faltan. Verifica tus variables de entorno.")
    exit(1)

# Inicializa el cliente
app = Client(
    name="stealer-phone",
    api_id=int(api_id),
    api_hash=api_hash,
    session_string=string_session
)

# Función principal
async def main():
    try:
        await app.start()
        me = await app.get_me()
        logging.info(f"✅ Conectado como: {me.first_name} (@{me.username}) - ID: {me.id}")
        # Tu lógica principal iría aquí...
        await app.idle()
    except (SessionPasswordNeeded, ApiIdInvalid, PhoneNumberInvalid) as e:
        logging.error(f"❌ Error en autenticación: {str(e)}")
        exit(1)
    except Exception as e:
        logging.error(f"⚠️ Excepción inesperada: {str(e)}")
        exit(1)
    finally:
        await app.stop()
        logging.info("🛑 Sesión finalizada correctamente.")

# Ejecuta
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
