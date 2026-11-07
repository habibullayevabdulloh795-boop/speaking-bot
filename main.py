import os
import logging
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiohttp import web

TOKEN = "9277763375:AAERJcrUV7du3pQPmhohGVnEOvd1SFVJ72Y"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    builder = types.InlineKeyboardBuilder()
    web_app_url = "https://speaking-bot.onrender.com"
    
    builder.row(types.InlineKeyboardButton(
        text="🚀 Open App (Speaking Platforma)", 
        web_app=types.WebAppInfo(url=web_app_url)
    ))
    
    await message.answer(
        f"Assalomu alaykum, {message.from_user.first_name}!\n"
        "Speaking mashg'ulot botiga xush kelibsiz.\n\n"
        "Quyidagi tugmani bosib Web Mini App'ga kiring:",
        reply_markup=builder.as_markup()
    )

async def handle_index(request):
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        return web.Response(text=html_content, content_type='text/html')
    except Exception as e:
        return web.Response(text=f"Xatolik: {str(e)}", status=500)

async def web_server():
    app = web.Application()
    app.router.add_get('/', handle_index)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

async def main():
    await web_server()
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
