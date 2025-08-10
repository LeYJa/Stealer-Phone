import asyncio
from aiohttp import web
from yourbotmodule import start_userbot  # 👈 ajusta esto si tu función tiene otro nombre o está en otro archivo

# 🔗 Servidor HTTP para Fly.io
async def start_http():
    app = web.Application()
    app.router.add_get("/", lambda _: web.Response(text="OK"))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8080)
    await site.start()

# 🧵 Correr todo a la vez
async def main():
    await asyncio.gather(
        start_http(),    # servidor web
        start_userbot()  # tu bot principal
    )

if __name__ == "__main__":
    asyncio.run(main())
