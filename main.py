import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiohttp import web

# Tokenni xavfsiz tarzda Environment'dan yoki to'g'ridan-to'g'ri o'qish
TOKEN = os.getenv("BOT_TOKEN", "9277763375:AAHE_Kjhbo6aGkkM1Jvrz_7Rlb4MPQOVZ0s")

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    builder = types.InlineKeyboardBuilder()
    web_app_url = "https://speaking-bot-wakv.onrender.com"
    builder.add(types.InlineKeyboardButton(
        text="🚀 Open App",
        web_app=types.WebAppInfo(url=web_app_url)
    ))
    await message.answer(
        "Assalomu alaykum! Speaking platformamizga xush kelibsiz. 20 ta Full Mock testlar, xatolar tahlili va AI feedback'dan foydalanish uchun quyidagi tugmani bosing:",
        reply_markup=builder.as_markup()
    )

# Render uchun veb-server (404 xatoligini oldini olib index.html ni ochadi)
async def handle_index(request):
    try:
        return web.FileResponse('index.html')
    except Exception as e:
        return web.Response(text=f"Platform ishga tushdi, lekin index.html topilmadi: {e}", status=404)

async def web_server():
    app = web.Application()
    app.router.add_get('/', handle_index)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    logging.info(f"Veb-server {port}-portda ishga tushdi!")

async def main():
    # Veb-server va Telegram bot polling jarayonini birga yurgizish
    await web_server()
    logging.info("Telegram bot polling boshlandi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
