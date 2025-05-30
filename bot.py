import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
import os

API_TOKEN = os.getenv("API_TOKEN")
if not API_TOKEN:
    raise ValueError("API_TOKEN не найден. Убедись, что переменная окружения установлена.")

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Список врачей
doctors = {
    "🧑‍⚕️ Анварбек": "https://t.me/+998900619976",
    "👨‍⚕️ Зокиров": "https://t.me/+998901470208",
    "👨‍⚕️ Доктор Сидоров": "https://t.me/doctor_sidorov",
}

# Главное меню
def main_menu():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📋 Список врачей", callback_data="show_doctors")],
    ])
    return keyboard

# Клавиатура со списком врачей
def doctor_list():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=name, url=link)] for name, link in doctors.items()
    ])

# Стартовое сообщение
@dp.message(CommandStart())
async def start_cmd(message: Message):
    text = (
        f"👋 Привет, {message.from_user.first_name}!\n\n"
        "Добро пожаловать в бот записи к врачам.\n"
        "Выберите нужный пункт меню ниже 👇"
    )
    await message.answer(text, reply_markup=main_menu())

# Обработка нажатий на кнопки
@dp.callback_query()
async def callbacks(call: CallbackQuery):
    if call.data == "show_doctors":
        await call.message.edit_text("🧾 Вот список доступных специалистов:", reply_markup=doctor_list())

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
