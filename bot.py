import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

API_TOKEN = "7936346773:AAE6WYPtp0POcgu_Tu8RmLhOJDlJ7-R5G2w"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

doctors = {
    "Анварбек": "https://t.me/anvarbek20",
    "Зокиров": "https://t.me/zokirovhb",
    "Доктор Сидоров": "https://t.me/doctor_sidorov",
}

@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    for name, link in doctors.items():
        keyboard.add(types.InlineKeyboardButton(text=name, url=link))
    await message.answer("Выберите человека из списка:", reply_markup=keyboard)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
