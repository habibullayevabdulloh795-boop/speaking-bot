import os

FILES = {}

FILES['.env'] = r'''BOT_TOKEN=9277763375:AAG0kK__ic4yAjHlTWRhPAACg9dwpEG1ULU
WEBAPP_URL=https://abdulloh.github.io/speaking-bot/
ADMIN_USERNAME=wty_12
'''

FILES['.env.example'] = r'''# @BotFather bergan token
BOT_TOKEN=9277763375:AAG0kK__ic4yAjHlTWRhPAACg9dwpEG1ULU
# GitHub Pages manzili (https bo'lishi shart)
WEBAPP_URL=https://abdulloh.github.io/speaking-bot/
# Admin username (@siz)
ADMIN_USERNAME=wty_12
'''

FILES['.gitignore'] = r'''.env
__pycache__/
*.pyc
.venv/
venv/
.idea/
.vscode/
'''

FILES['README.md'] = r'''# 🎤 Speaking Bot + Mini App

Telegram bot (aiogram 3) va Web Mini App (GitHub Pages) — IELTS/CEFR speaking mashqlari uchun.

## Tuzilishi## Ishga tushirish
1. `pip install -r requirements.txt`
2. `python main.py`
'''

FILES['bot/__init__.py'] = r''''''

FILES['bot/config.py'] = r'''"""Sozlamalar .env faylidan o'qiladi."""
import os
import sys

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
WEBAPP_URL = os.getenv("WEBAPP_URL", "").strip()
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "").strip().lstrip("@")

if not BOT_TOKEN:
    sys.exit("Xato: BOT_TOKEN .env faylida ko'rsatilmagan.")
if not WEBAPP_URL.startswith("https://"):
    sys.exit("Xato: WEBAPP_URL https:// bilan boshlanishi shart (Telegram talabi).")
'''

FILES['bot/handlers.py'] = r'''from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message

from . import texts
from .keyboards import main_menu, open_app_only

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    name = message.from_user.first_name if message.from_user else "do'st"
    await message.answer(texts.welcome(name), reply_markup=main_menu())
    await message.answer(texts.MOCK)
    await message.answer(texts.PARTS)
    await message.answer(texts.IDIOMS)


@router.message(Command("menu"))
async def cmd_menu(message: Message) -> None:
    await message.answer("Quyidagi bo'limlardan birini tanlang:", reply_markup=main_menu())


@router.callback_query(F.data == "mock")
async def cb_mock(call: CallbackQuery) -> None:
    await call.message.answer(texts.MOCK, reply_markup=open_app_only())
    await call.answer()


@router.callback_query(F.data == "parts")
async def cb_parts(call: CallbackQuery) -> None:
    await call.message.answer(texts.PARTS, reply_markup=open_app_only())
    await call.answer()


@router.callback_query(F.data == "ai")
async def cb_ai(call: CallbackQuery) -> None:
    await call.message.answer(texts.AI_CHAT, reply_markup=open_app_only())
    await call.answer()


@router.callback_query(F.data == "stats")
async def cb_stats(call: CallbackQuery) -> None:
    await call.message.answer(texts.STATS, reply_markup=open_app_only())
    await call.answer()


@router.callback_query(F.data == "idioms")
async def cb_idioms(call: CallbackQuery) -> None:
    await call.message.answer(texts.IDIOMS)
    await call.answer()


@router.callback_query(F.data == "admin")
async def cb_admin(call: CallbackQuery) -> None:
    await call.message.answer(texts.ADMIN)
    await call.answer()
'''

FILES['bot/keyboards.py'] = r'''from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

from .config import ADMIN_USERNAME, WEBAPP_URL


def main_menu() -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text="🌐 Open App (Speaking Platforma)",
                             web_app=WebAppInfo(url=WEBAPP_URL))],
        [InlineKeyboardButton(text="🎓 Full Mock Speaking (20 ta)",
                             callback_data="mock")],
        [InlineKeyboardButton(text="🧩 Alohida Partlar (1.1, 1.2, 2...)",
                             callback_data="parts")],
        [InlineKeyboardButton(text="🤖 AI bilan Gaplashish",
                             callback_data="ai")],
        [InlineKeyboardButton(text="📊 Darajam va Natijalarim",
                             callback_data="stats")],
        [InlineKeyboardButton(text="💡 C1 Idiomalar va Maslahatlar",
                             callback_data="idioms")],
    ]
    if ADMIN_USERNAME:
        rows.append([InlineKeyboardButton(
            text="📞 Admin bilan Bog'lanish",
            url=f"https://t.me/{ADMIN_USERNAME}")])
    else:
        rows.append([InlineKeyboardButton(
            text="📞 Admin bilan Bog'lanish", callback_data="admin")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def open_app_only() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="🚀 Open App", web_app=WebAppInfo(url=WEBAPP_URL))
    ]])
'''

FILES['bot/texts.py'] = r'''"""Bot matnlari bir joyda turadi, o'zgartirish oson bo'lishi uchun."""
from html import escape


def welcome(first_name: str) -> str:
    return (
        f"Assalomu alaykum, <i>{escape(first_name)}</i>!\n"
        "Speaking mashg'ulot botiga xush kelibsiz.\n\n"
        "Quyidagi bo'limlardan birini tanlang:"
    )


MOCK = (
    "🎓 Full Mock Speaking: 20 ta to'liq imtihon testi tayyorlanmoqda. "
    "Saytimiz orqali to'liq topshirishingiz mumkin!"
)

PARTS = (
    "🧩 Alohida Partlar: Part 1, Part 2 va Part 3 savollari bo'yicha mashq "
    "qilish uchun Mini App'ga kiring."
)

IDIOMS = (
    "💡 C1 Idiomalar va Maslahatlar:\n"
    "• <b>A blessing in disguise</b> — Yomon ko'ringan, lekin oxiri "
    "yaxshilikka olib keladigan holat.\n"
    "• <b>Hit the nail on the head</b> — Aynan topib gapirmoq."
)

AI_CHAT = (
    "🤖 AI bilan Gaplashish: tez orada ishga tushadi. "
    "Hozircha Mini App orqali mashq qilishingiz mumkin."
)

STATS = (
    "📊 Darajam va Natijalarim: natijalaringiz Mini App ichida "
    "ko'rsatiladi."
)

ADMIN = "📞 Admin bilan bog'lanish uchun pastdagi tugmani bosing."
'''

FILES['docs/index.html'] = r'''<!DOCTYPE html>
<html lang="uz">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Speaking Platforma</title>
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<style>
  :root {
    --bg: var(--tg-theme-bg-color, #17212b);
    --card: var(--tg-theme-secondary-bg-color, #232e3c);
    --text: var(--tg-theme-text-color, #f5f5f5);
    --hint: var(--tg-theme-hint-color, #8b9aaa);
    --accent: var(--tg-theme-button-color, #2ea6ff);
    --accent-text: var(--tg-theme-button-text-color, #fff);
  }
  * { box-sizing: border-box; margin: 0; }
  body {
    font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
    background: var(--bg); color: var(--text);
    padding: 16px 16px 90px; min-height: 100vh;
  }
  h1 { font-size: 20px; }
  .sub { color: var(--hint); font-size: 14px; margin: 4px 0 18px; }
  .tabs { display: flex; gap: 8px; overflow-x: auto; margin-bottom: 16px; }
  .tab {
    flex: none; padding: 9px 14px; border-radius: 20px; border: 0;
    background: var(--card); color: var(--text); font-size: 14px; cursor: pointer;
  }
  .tab.active { background: var(--accent); color: var(--accent-text); }
  .card {
    background: var(--card); border-radius: 14px; padding: 14px 16px;
    margin-bottom: 10px;
  }
  .card h3 { font-size: 15px; margin-bottom: 4px; }
  .card p { font-size: 14px; color: var(--hint); line-height: 1.45; }
  .btn {
    margin-top: 10px; padding: 8px 14px; border: 0; border-radius: 10px;
    background: var(--accent); color: var(--accent-text); font-size: 13px; cursor: pointer;
  }
  .hidden { display: none; }
</style>
</head>
<body>
  <h1>🌐 Speaking Platforma</h1>
  <div class="sub" id="hello">Xush kelibsiz!</div>

  <div class="tabs" id="tabs">
    <button class="tab active" data-tab="mock">🎓 Full Mock</button>
    <button class="tab" data-tab="parts">🧩 Partlar</button>
    <button class="tab" data-tab="idioms">💡 Idiomalar</button>
    <button class="tab" data-tab="stats">📊 Natijalar</button>
  </div>

  <section id="mock"></section>
  <section id="parts" class="hidden"></section>
  <section id="idioms" class="hidden"></section>
  <section id="stats" class="hidden"></section>

<script>
const tg = window.Telegram?.WebApp;
if (tg) {
  tg.ready();
  tg.expand();
  const u = tg.initDataUnsafe?.user;
  if (u) document.getElementById("hello").textContent = `Salom, ${u.first_name}!`;
}

const PARTS = [
  { id: "1.1", title: "Part 1.1", desc: "Shaxsiy savollar: uy, ish, o'qish, hobbilar.",
    questions: ["Do you work or are you a student?", "What do you like most about your hometown?"] },
  { id: "1.2", title: "Part 1.2", desc: "Kundalik hayot va odatlar haqida savollar.",
    questions: ["How do you usually spend your weekends?", "Do you prefer mornings or evenings?"] },
  { id: "2", title: "Part 2", desc: "Cue card: 1-2 daqiqa mavzu bo'yicha gapirish.",
    questions: ["Describe a book that you enjoyed reading."] },
  { id: "3", title: "Part 3", desc: "Part 2 mavzusi bo'yicha chuqur muhokama.",
    questions: ["Why do some people read more than others?"] },
];

const IDIOMS = [
  { en: "A blessing in disguise", uz: "Yomon ko'ringan, lekin oxiri yaxshilikka olib keladigan holat." },
  { en: "Hit the nail on the head", uz: "Aynan topib gapirmoq." },
  { en: "Once in a blue moon", uz: "Juda kamdan-kam holda." },
  { en: "Break the ice", uz: "Notanish odamlar orasida suhbatni boshlab yuborish." },
];

const MOCK_COUNT = 20;
const $ = id => document.getElementById(id);

$("mock").innerHTML = Array.from({ length: MOCK_COUNT }, (_, i) => `
  <div class="card">
    <h3>Mock Test #${i + 1}</h3>
    <p>Part 1 + Part 2 + Part 3 (taxminan 14 daqiqa)</p>
    <button class="btn" onclick="startTimer(${i + 1})">Boshlash</button>
  </div>`).join("");

$("parts").innerHTML = PARTS.map(p => `
  <div class="card">
    <h3>${p.title}</h3>
    <p>${p.desc}</p>
    <button class="btn" onclick="showQuestion('${p.id}')">Tasodifiy savol</button>
  </div>`).join("");

$("idioms").innerHTML = IDIOMS.map(i => `
  <div class="card"><h3>${i.en}</h3><p>${i.uz}</p></div>`).join("");

function renderStats() {
  const done = JSON.parse(localStorage.getItem("done") || "[]");
  $("stats").innerHTML = `
    <div class="card"><h3>Yakunlangan mocklar</h3>
    <p>${done.length} / ${MOCK_COUNT}</p></div>`;
}
renderStats();

$("tabs").addEventListener("click", e => {
  const btn = e.target.closest(".tab"); if (!btn) return;
  document.querySelectorAll(".tab").forEach(t => t.classList.toggle("active", t === btn));
  ["mock", "parts", "idioms", "stats"].forEach(id =>
    $(id).classList.toggle("hidden", id !== btn.dataset.tab));
  tg?.HapticFeedback?.selectionChanged();
});

function showQuestion(id) {
  const p = PARTS.find(x => x.id === id);
  const q = p.questions[Math.floor(Math.random() * p.questions.length)];
  tg?.showAlert ? tg.showAlert(q) : alert(q);
}

let timerId;
function startTimer(n) {
  clearInterval(timerId);
  let sec = 14 * 60;
  const msg = () => `Mock #${n}\n${String(Math.floor(sec / 60)).padStart(2, "0")}:${String(sec % 60).padStart(2, "0")}`;
  tg?.MainButton?.setParams({ text: "Mock #" + n + " yakunlash", is_visible: true });
  tg?.MainButton?.onClick(() => finishMock(n));
  timerId = setInterval(() => {
    sec--;
    tg?.MainButton?.setText(msg().replace("\n", " · "));
    if (sec <= 0) { clearInterval(timerId); finishMock(n); }
  }, 1000);
}
function finishMock(n) {
  clearInterval(timerId);
  const done = new Set(JSON.parse(localStorage.getItem("done") || "[]"));
  done.add(n);
  localStorage.setItem("done", JSON.stringify([...done]));
  tg?.MainButton?.hide();
  renderStats();
}
</script>
</body>
</html>
'''

FILES['main.py'] = r'''import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand, MenuButtonWebApp, WebAppInfo

from bot.config import BOT_TOKEN, WEBAPP_URL
from bot.handlers import router


async def main() -> None:
    logging.basicConfig(level=logging.INFO)

    bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.include_router(router)

    await bot.set_my_commands([
        BotCommand(command="start", description="Botni ishga tushirish"),
        BotCommand(command="menu", description="Asosiy menyu"),
    ])
    await bot.set_chat_menu_button(
        menu_button=MenuButtonWebApp(text="Open App", web_app=WebAppInfo(url=WEBAPP_URL))
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
'''

FILES['requirements.txt'] = r'''aiogram>=3.13,<4
python-dotenv>=1.0
'''

ROOT = "speaking-bot"
for path, content in FILES.items():
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print("yaratildi:", full)

print("\nTayyor! Ishga tushirish uchun:")
print("1. cd speaking-bot")
print("2. pip install -r requirements.txt")
print("3. python main.py")
