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

# Врачи и ссылки
doctors = {
    "🧑‍⚕️ Анварбек": "https://t.me/+998900619976",
    "👨‍⚕️ Зокиров": "https://t.me/+998901470208",
    "👨‍⚕️ Доктор Сидоров": "https://t.me/doctor_sidorov",
}

# Главное меню
def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📋 Список врачей", callback_data="show_doctors")],
    ])

# Меню с врачами + кнопка Назад
def doctor_list():
    keyboard = [
        [InlineKeyboardButton(text=name, url=link)] for name, link in doctors.items()
    ]
    keyboard.append([InlineKeyboardButton(text="◀ Назад в меню", callback_data="go_back")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

# Приветствие
@dp.message(CommandStart())
async def start_cmd(message: Message):
    await message.answer(
        f"👋 Привет, {message.from_user.first_name}!\n\n"
        "Я помогу тебе связаться с нужным врачом.",
        reply_markup=main_menu()
    )

# Обработка кнопок
@dp.callback_query()
async def handle_callback(call: CallbackQuery):
    if call.data == "show_doctors":
        await call.message.edit_text("🧾 Вот список врачей:", reply_markup=doctor_list())
    elif call.data == "go_back":
        await call.message.edit_text("🔙 Вы вернулись в главное меню.", reply_markup=main_menu())

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
