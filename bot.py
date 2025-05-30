import asyncio
import aiosqlite
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message
import os

API_TOKEN = os.getenv("API_TOKEN")
if not API_TOKEN:
    raise ValueError("API_TOKEN не найден. Убедись, что переменная окружения установлена.")

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

ADMIN_ID = 5409762556  # <-- замени на свой user_id числом

DB_PATH = "doctors.db"

# --- Инициализация базы данных
async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS doctors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                link TEXT NOT NULL
            )
        """)
        await db.commit()

# --- Получить список врачей из БД
async def get_doctors():
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT id, name, link FROM doctors")
        rows = await cursor.fetchall()
        return rows

# --- Добавить врача в БД
async def add_doctor(name: str, link: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("INSERT INTO doctors (name, link) VALUES (?, ?)", (name, link))
        await db.commit()

# --- Удалить врача по id
async def delete_doctor(doc_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM doctors WHERE id = ?", (doc_id,))
        await db.commit()

# --- Клавиатура главного меню
def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📋 Список врачей", callback_data="show_doctors")],
        [InlineKeyboardButton(text="❓ Помощь", callback_data="help")],
    ])

# --- Клавиатура со списком врачей (с кнопками удаления для админа)
async def doctor_list_keyboard(is_admin=False):
    doctors = await get_doctors()
    keyboard = []
    for doc_id, name, link in doctors:
        row = [InlineKeyboardButton(text=name, url=link)]
        if is_admin:
            # Кнопка удаления врача (callback_data с id врача)
            row.append(InlineKeyboardButton(text="❌ Удалить", callback_data=f"delete_{doc_id}"))
        keyboard.append(row)
    keyboard.append([InlineKeyboardButton(text="◀ Назад в меню", callback_data="go_back")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

# --- Команда /start
@dp.message(CommandStart())
async def start_cmd(message: Message):
    await message.answer(
        f"👋 Привет, {message.from_user.first_name}!\n"
        "Я помогу тебе связаться с нужным врачом.\n\n"
        "Используй кнопки ниже для навигации.",
        reply_markup=main_menu()
    )

# --- Обработка нажатий кнопок
@dp.callback_query()
async def handle_callback(call: CallbackQuery):
    user_id = call.from_user.id

    if call.data == "show_doctors":
        kb = await doctor_list_keyboard(is_admin=(user_id == ADMIN_ID))
        await call.message.edit_text("🧾 Вот список врачей:", reply_markup=kb)
        await call.answer()
    elif call.data == "go_back":
        await call.message.edit_text("🔙 Вы вернулись в главное меню.", reply_markup=main_menu())
        await call.answer()
    elif call.data == "help":
        await call.message.answer(
            "❓ Помощь\n"
            "Используй кнопки для навигации по боту.\n"
            "Если нужна дополнительная информация — пиши сюда."
        )
        await call.answer()
    elif call.data.startswith("delete_") and user_id == ADMIN_ID:
        # Удаление врача
        doc_id = int(call.data.split("_")[1])
        await delete_doctor(doc_id)
        kb = await doctor_list_keyboard(is_admin=True)
        await call.message.edit_text("🧾 Врач удалён. Обновлённый список врачей:", reply_markup=kb)
        await call.answer("Врач удалён")
    else:
        await call.answer("Неизвестная команда", show_alert=True)

# --- Админ: Добавление врача через команды
# Ожидаем от админа сообщение с именем врача
adding_name = set()
adding_link = dict()

@dp.message(Command("adddoctor"))
async def add_doctor_start(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.reply("У вас нет доступа к этой команде.")
        return
    await message.reply("Введите имя врача:")
    adding_name.add(message.from_user.id)

@dp.message()
async def process_doctor_name(message: Message):
    if message.from_user.id in adding_name:
        adding_link[message.from_user.id] = None
        adding_name.remove(message.from_user.id)
        adding_link[message.from_user.id] = {'name': message.text}
        await message.reply("Введите ссылку на врача (Telegram или веб-ссылку):")
        return

    if message.from_user.id in adding_link and adding_link[message.from_user.id]['name'] and adding_link[message.from_user.id].get('link') is None:
        name = adding_link[message.from_user.id]['name']
        link = message.text
        await add_doctor(name, link)
        await message.reply(f"✅ Врач '{name}' добавлен.")
        adding_link.pop(message.from_user.id)
        return

# --- Перехват любых сообщений для пересылки админу (кроме команд /start)
@dp.message()
async def forward_user_message(message: Message):
    if message.text and not message.text.startswith("/start") and message.from_user.id != ADMIN_ID:
        await bot.send_message(
            ADMIN_ID,
            f"Сообщение от @{message.from_user.username or message.from_user.id}:\n{message.text}"
        )

async def main():
    await init_db()

    # Если база пуста - добавим тестовых врачей
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT COUNT(*) FROM doctors")
        count = (await cursor.fetchone())[0]
        if count == 0:
            await db.execute("INSERT INTO doctors (name, link) VALUES (?, ?)", ("🧑‍⚕️ Анварбек", "https://t.me/+998900619976"))
            await db.execute("INSERT INTO doctors (name, link) VALUES (?, ?)", ("👨‍⚕️ Зокиров", "https://t.me/+998901470208"))
            await db.execute("INSERT INTO doctors (name, link) VALUES (?, ?)", ("👨‍⚕️ Доктор Сидоров", "https://t.me/doctor_sidorov"))
            await db.commit()

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
