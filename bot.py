from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Кнопки для Reply Keyboard (отдельно от Inline)
def reply_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📋 Список врачей")],
            [KeyboardButton(text="❓ Помощь")],
        ],
        resize_keyboard=True
    )
    return keyboard

@dp.message(CommandStart())
async def start_cmd(message: Message):
    await message.answer(
        f"👋 Привет, {message.from_user.first_name}!\n\n"
        "Я помогу тебе связаться с нужным врачом.\n\n"
        "Используй кнопки ниже для навигации.",
        reply_markup=reply_keyboard()
    )

# Обработка нажатия Reply кнопок (тексты сообщений)
@dp.message()
async def reply_keyboard_handler(message: Message):
    if message.text == "📋 Список врачей":
        await message.answer("🧾 Вот список врачей:", reply_markup=doctor_list())
    elif message.text == "❓ Помощь":
        await message.answer(
            "❓ *Помощь*\n"
            "Используй кнопки для навигации по боту.\n"
            "Если нужна дополнительная информация, пиши сюда.",
            parse_mode="Markdown",
            reply_markup=reply_keyboard()
        )
    else:
        await message.answer("Я не понимаю эту команду. Пожалуйста, выбери кнопку из меню.", reply_markup=reply_keyboard())
