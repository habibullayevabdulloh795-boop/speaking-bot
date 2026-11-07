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

# 1. /start bosganda darajalar va Open App tugmasini chiqarish
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    builder = types.InlineKeyboardBuilder()
    web_app_url = "https://speaking-bot-wakv.onrender.com"
    
    # Tugmalarni xuddi o'sha ikkinchi skrinshotdagidek qilib joylaymiz
    builder.row(
        types.InlineKeyboardButton(text="🟢 A2", callback_data="level_A2"),
        types.InlineKeyboardButton(text="🔵 B1", callback_data="level_B1")
    )
    builder.row(
        types.InlineKeyboardButton(text="🟠 B2", callback_data="level_C1"), # xohlasangiz moslab olasiz
        types.InlineKeyboardButton(text="🔥 C1", callback_data="level_C1")
    )
    builder.row(
        types.InlineKeyboardButton(text="🚀 Open App (Speaking Platforma)", web_app=types.WebAppInfo(url=web_app_url))
    )
    
    await message.answer(
        "Assalomu alaykum, Abdulloh!\nSpeaking mashg'ulot botiga xush kelibsiz.\n\nTayyorgarlik ko'rmoqchi bo'lgan darajangizni tanlang:",
        reply_markup=builder.as_markup()
    )

@dp.callback_query()
async def callback_handler(callback: types.CallbackQuery):
    await callback.message.answer(f"Siz darajani tanladingiz! Endi 'Open App' tugmasi orqali platformaga kiring 🚀")
    await callback.answer()

# 2. Render uchun veb-server (Open App bosganda index.html ni ochadi)
async def handle_index(request):
    try:
        return web.FileResponse('index.html')
    except Exception as e:
        return web.Response(text=f"index.html topilmadi: {e}", status=404)

async def main():
    app = web.Application()
    app.router.add_get('/', handle_index)
    
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()

    # Webhookni tozalab pollingni boshlash
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
