import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiohttp import web

TOKEN = "9277763375:AAHE_Kjhbo6aGkkM1Jvrz_7Rlb4MPQOVZ0s"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Assalomu alaykum! Bot muvaffaqiyatli ishga tushdi! 🚀")

async def handle(request):
    return web.Response(text="Bot is running!")

async def main():
    # Render port talabi uchun veb-server
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()

    # Eng muhimi: oldingi qolib ketgan webhookni o'chirish
    await bot.delete_webhook(drop_pending_updates=True)

    # Telegram bot polling
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
