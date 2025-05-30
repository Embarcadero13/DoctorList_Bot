import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import (
    Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery,
    ReplyKeyboardMarkup, KeyboardButton
)
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

# Главное меню с Inline-кнопками
def main_menu_inline():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📋 Список врачей", callback_data="show_doctors")],
    ])

# Меню с врачами + кнопка Назад (Inline)
def doctor_list():
    keyboard = [
        [InlineKeyboardButton(text=name, url=link)] for name, link in doctors.items()
    ]
    keyboard.append([InlineKeyboardButton(text="◀ Назад в меню", callback_data="go_back")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

# Reply Keyboard (кнопки под полем ввода)
def main_menu_reply():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📋 Список врачей")],
            [KeyboardButton(text="❓ Помощь")],
        ],
        resize_keyboard=True
    )
    return keyboard

# Обработчик команды /start
@dp.message(CommandStart())
async def start_cmd(message: Message):
    await message.answer(
        f"👋 Привет, {message.from_user.first_name}!\n\n"
        "Я помогу тебе связаться с нужным врачом.\n\n"
        "Используй кнопки ниже для навигации.",
        reply_markup=main_menu_reply()
    )

# Обработка нажатия Reply Keyboard кнопок
@dp.message()
async def reply_keyboard_handler(message: Message):
    if message.text == "📋 Список врачей":
        await message.answer("🧾 Вот список врачей:", reply_markup=doctor_list())
    elif message.text == "❓ Помощь":
        await message.answer(
            "❓ *Помощь*\n"
            "Используй кнопки для навигации по боту.\n"
            "Если нужна дополнительная информация — пиши сюда.",
            parse_mode="Markdown",
            reply_markup=main_menu_reply()
        )
    else:
        await message.answer(
            "⚠️ Я не понимаю эту команду. Пожалуйста, выбери кнопку из меню.",
            reply_markup=main_menu_reply()
        )

# Обработка Inline-кнопок
@dp.callback_query()
async def handle_callback(call: CallbackQuery):
    if call.data == "show_doctors":
        await call.message.edit_text("🧾 Вот список врачей:", reply_markup=doctor_list())
    elif call.data == "go_back":
        await call.message.edit_text("🔙 Вы вернулись в главное меню.", reply_markup=main_menu_inline())

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
