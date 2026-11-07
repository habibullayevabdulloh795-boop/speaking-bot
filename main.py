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

# 1. Telegram bot: /start bosganda barcha kerakli menyularni chiqarish
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    builder = types.InlineKeyboardBuilder()
    web_app_url = "https://speaking-bot-wakv.onrender.com"
    
    # Barcha asosiy menyu tugmalari
    builder.row(types.InlineKeyboardButton(text="🌐 Open App (Speaking Platforma)", web_app=types.WebAppInfo(url=web_app_url)))
    builder.row(types.InlineKeyboardButton(text="🎓 Full Mock Speaking (20 ta)", callback_data="full_mock"))
    builder.row(types.InlineKeyboardButton(text="🧩 Alohida Partlar (1.1, 1.2, 2...)", callback_data="parts"))
    builder.row(types.InlineKeyboardButton(text="🤖 AI bilan Gaplashish", callback_data="ai_chat"))
    builder.row(types.InlineKeyboardButton(text="📊 Darajam va Natijalarim", callback_data="results"))
    builder.row(types.InlineKeyboardButton(text="💡 C1 Idiomalar va Maslahatlar", callback_data="idioms"))
    builder.row(types.InlineKeyboardButton(text="📞 Admin bilan Bog'lanish", callback_data="admin"))
    
    await message.answer(
        f"Assalomu alaykum, __{message.from_user.first_name}__!\nSpeaking mashg'ulot botiga xush kelibsiz.\n\nQuyidagi bo'limlardan birini tanlang:",
        reply_markup=builder.as_markup(),
        parse_mode="Markdown"
    )

@dp.callback_query()
async def callback_handler(callback: types.CallbackQuery):
    await callback.message.answer("Tanlangan bo'lim tez orada ishga tushadi 🚀")
    await callback.answer()

# 2. Veb-server: brauzerdan yoki Mini App'dan kirganda to'g'ridan-to'g'ri index.html ni ochadi
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
