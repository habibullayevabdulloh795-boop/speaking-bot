import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

TOKEN = "9277763375:AAHE_Kjhbo6aGkkM1Jvrz_7Rlb4MPQOVZ0s"
WEBHOOK_URL = "https://speaking-bot-wakv.onrender.com"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    builder = types.InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="🌐 Open App (Speaking Platforma)", web_app=types.WebAppInfo(url=WEBHOOK_URL)))
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

async def handle_index(request):
    try:
        return web.FileResponse('index.html')
    except Exception as e:
        return web.Response(text=f"index.html topilmadi: {e}", status=404)

async def on_startup(bot: Bot):
    await bot.set_webhook(f"{WEBHOOK_URL}/webhook", drop_pending_updates=True)

def main():
    app = web.Application()
    app.router.add_get('/', handle_index)
    
    # Webhook handler for Telegram bot
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
    )
    webhook_requests_handler.register(app, path="/webhook")
    setup_application(app, dp, bot=bot)
    
    dp.startup.register(on_startup)
    
    port = int(os.environ.get("PORT", 10000))
    web.run_app(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()
