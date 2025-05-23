import asyncio
from aiogram import Bot, Dispatcher, types
import os

API_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

doctors = {
    "Анварбек": "https://t.me/anvarbek20",
    "Зокиров": "https://t.me/zokirovhb",
    "Доктор Сидоров": "https://t.me/doctor_sidorov",
}

@dp.message(commands=["start"])
async def send_welcome(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    for name, link in doctors.items():
        keyboard.add(types.InlineKeyboardButton(text=name, url=link))
    await message.answer("Выберите человека из списка:", reply_markup=keyboard)

async def main():
    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())
