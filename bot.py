import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command
import os

API_TOKEN = os.getenv("API_TOKEN")

if not API_TOKEN:
    raise ValueError("API_TOKEN не найден. Убедись, что переменная окружения установлена.")

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

doctors = {
    "Анварбек": "https://t.me/anvarbek20",
    "Зокиров": "https://t.me/zokirovhb",
    "Доктор Сидоров": "https://t.me/doctor_sidorov",
}

@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=name, url=link)] for name, link in doctors.items()]
    )
    await message.answer("Выберите человека из списка:", reply_markup=keyboard)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
