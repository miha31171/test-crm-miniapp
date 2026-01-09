# bot.py
import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, types, F
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import ReplyKeyboardBuilder

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN") or "8533195567:AAEwvlMQZ13kGcKMFVwHA11Smh07mwy9EoY"

# Укажи сюда HTTPS‑URL мини‑приложения
WEBAPP_URL = os.getenv("WEBAPP_URL") or "https://your-domain.com/"

bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    kb = ReplyKeyboardBuilder()
    kb.add(
        types.KeyboardButton(
            text="Открыть CRM",
            web_app=types.WebAppInfo(url=WEBAPP_URL),
        )
    )
    await message.answer(
        "Открой мини‑CRM для создания записи и просмотра ближайших сеансов.",
        reply_markup=kb.as_markup(resize_keyboard=True),
    )

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
