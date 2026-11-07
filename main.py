import asyncio
import logging
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardRemove

TOKEN = "9277763375:AAERJcrUV7du3pQPmhohGVnEOvdlSFVJ72Y"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(text="🟢 A2", callback_data="level_a2"),
        types.InlineKeyboardButton(text="🔵 B1", callback_data="level_b1"),
    )
    builder.row(
        types.InlineKeyboardButton(text="🟠 B2", callback_data="level_b2"),
        types.InlineKeyboardButton(text="🔥 C1", callback_data="level_c1"),
    )
    
    await message.answer(
        f"Assalomu alaykum, _{message.from_user.first_name}_!\n"
        "Speaking mashg'ulot botiga xush kelibsiz.\n\n"
        "Tayyorgarlik ko'rmoqchi bo'lgan darajangizni tanlang:",
        reply_markup=ReplyKeyboardRemove()
    )
    await message.answer(
        "Quyidagi darajalardan birini tanlang:",
        reply_markup=builder.as_markup(),
        parse_mode="Markdown"
    )

@dp.callback_query(F.data == "main_menu")
async def back_to_menu(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(text="🟢 A2", callback_data="level_a2"),
        types.InlineKeyboardButton(text="🔵 B1", callback_data="level_b1"),
    )
    builder.row(
        types.InlineKeyboardButton(text="🟠 B2", callback_data="level_b2"),
        types.InlineKeyboardButton(text="🔥 C1", callback_data="level_c1"),
    )
    
    await callback.message.edit_text(
        "🏠 **Asosiy menyu**\n\n"
        "Tayyorgarlik ko'rmoqchi bo'lgan darajangizni tanlang:",
        reply_markup=builder.as_markup(),
        parse_mode="Markdown"
    )
    await callback.answer()

@dp.callback_query(F.data.startswith("level_"))
async def select_level(callback: types.CallbackQuery):
    level = callback.data.split("_")[1].upper()
    
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="🚀 Open App (Speaking Platforma) 🌐", url="https://t.uz/webapp_or_site"))
    builder.row(
        types.InlineKeyboardButton(text="🎓 Full Mock Speaking (20 ta)", callback_data="full_mock"),
        types.InlineKeyboardButton(text="🧩 Alohida Partlar (1.1, 1.2, 2, 3)", callback_data="parts")
    )
    builder.row(
        types.InlineKeyboardButton(text="🤖 AI bilan Gaplashish (Limitsiz)", callback_data="ai_chat"),
        types.InlineKeyboardButton(text="📊 Darajam va Natijalarim (75 ball)", callback_data="my_results")
    )
    builder.row(types.InlineKeyboardButton(text="💡 C1 Idiomalar va Maslahatlar", callback_data="tips"))
    builder.row(types.InlineKeyboardButton(text="📞 Admin bilan Bog'lanish", url="https://t.me/wty_12"))
    builder.row(types.InlineKeyboardButton(text="🏠 Bosh menyu", callback_data="main_menu"))

    await callback.message.edit_text(
        f"Siz **{level}** darajasini tanladingiz! 🎯\n\n"
        "Quyidagi bo'limlardan birini tanlang:",
        reply_markup=builder.as_markup(),
        parse_mode="Markdown"
    )
    await callback.answer()

@dp.callback_query(F.data == "tips")
async def show_tips(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="🏠 Bosh menyu", callback_data="main_menu"))

    tips_text = (
        "💡 **Speaking'ni 75+ ballga ko'tarish uchun sirlar:**\n\n"
        "1. **Collocation'lar ishlating:** Oddiy *'very good'* deyish o'rniga *'highly beneficial'* yoki *'utmost importance'* deng.\n"
        "2. **Idiomalar qo'shing:** Masalan, *'once in a blue moon'* yoki *'hit the nail on the head'.*\n"
        "3. **Pauza qilmang:** O'ylab qolmasdan, *'Well, that's an interesting question...'*, *'As far as I'm concerned...'* kabi bog'lovchi iboralardan foydalaning.\n\n"
        "🎯 Har bir javobingizni aniq dalillar va shaxsiy tajriba bilan boyiting!"
    )
    await callback.message.edit_text(tips_text, reply_markup=builder.as_markup(), parse_mode="Markdown")
    await callback.answer()

async def main():
    print("Bot muvaffaqiyatli ishga tushdi va ishlamoqda...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
