import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
import os

API_TOKEN = os.getenv("API_TOKEN")
if not API_TOKEN:
    raise ValueError("API_TOKEN не найден. Убедись, что переменная окружения установлена.")

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Твой Telegram ID, чтобы получать уведомления (вставь сюда свой)
ADMIN_ID = 123456789  # <-- замени на свой настоящий Telegram user_id (число)

doctors = {
    "🧑‍⚕️ Анварбек": "https://t.me/+998900619976",
    "👨‍⚕️ Зокиров": "https://t.me/+998901470208",
    "👨‍⚕️ Доктор Сидоров": "https://t.me/doctor_sidorov",
}

def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📋 Список врачей", callback_data="show_doctors")],
        [InlineKeyboardButton(text="❓ Помощь", callback_data="help")]
    ])

def doctor_list():
    keyboard = [
        [InlineKeyboardButton(text=name, url=link)] for name, link in doctors.items()
    ]
    keyboard.append([InlineKeyboardButton(text="◀ Назад в меню", callback_data="go_back")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

@dp.message(CommandStart())
async def start_cmd(message: Message):
    try:
        await message.delete()
    except Exception:
        pass
    await message.answer(
        f"👋 Привет, {message.from_user.first_name}!\n\n"
        "Я помогу тебе связаться с нужным врачом.\n\n"
        "Используй кнопки ниже для навигации.",
        reply_markup=main_menu()
    )

@dp.callback_query()
async def handle_callback(call: CallbackQuery):
    if call.data == "show_doctors":
        await call.message.edit_text("🧾 Вот список врачей:", reply_markup=doctor_list())
    elif call.data == "go_back":
        await call.message.edit_text("🔙 Вы вернулись в главное меню.", reply_markup=main_menu())
    elif call.data == "help":
        await call.message.answer(
            "❓ Помощь\n"
            "Используй кнопки для навигации по боту.\n"
            "Если нужна дополнительная информация — пиши сюда."
        )
        # Уведомление админу, что пользователь запросил помощь
        await bot.send_message(ADMIN_ID, f"Пользователь @{call.from_user.username or call.from_user.id} запросил помощь.")

# Перехват любых сообщений, чтобы пересылать их админу (кроме команд /start)
@dp.message()
async def forward_user_message(message: Message):
    if message.text and not message.text.startswith("/start"):
        await bot.send_message(ADMIN_ID,
            f"Сообщение от @{message.from_user.username or message.from_user.id}:\n{message.text}"
        )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
