import sqlite3
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.for_validate import get_yes_no_kb


router = Router()

# Подключение к базе данных
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Создание таблицы пользователей (id, номер телефона и количество поинтов)
cursor.execute('''CREATE TABLE IF NOT EXISTS users
                  (user_id INTEGER PRIMARY KEY, vpn_number INT, points INT)''')
conn.commit()


@router.message(Command("start"))
async def cmd_start(message: Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name

    # Проверка наличия пользователя в базе данных
    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    existing_user = cursor.fetchone()

    if existing_user:
        vpn_number = existing_user[1]  # Получаем номер из базы данных
        points = existing_user[2]  # Получаем количество поинтов из базы данных
        await message.answer(f'Привет, {user_name}! Ты уже в нашей базе данных.')
        await message.answer(f'Твой номер: {vpn_number}. Твои поинты: {points}.')
        await message.answer('Если хочешь поменять свой номер, просто введи новый!')
    else:
        await message.answer(f'Привет, {user_name}! Ты попал в бота "того самого ВПНа.')
        await message.answer(f'Напиши свой номер.', reply_markup=ReplyKeyboardRemove())


# https://docs.aiogram.dev/en/dev-3.x/dispatcher/finite_state_machine/index.html <-- ПОСМОТРЕТЬ ТУТ

@router.message(F.text.isdigit())
async def get_num(message: Message):
    vpn_number = message.text

    await message.answer(f"Твой номер {vpn_number}?", reply_markup=get_yes_no_kb())


@router.message(F.text.lower() == "да")
async def answer_yes(message: Message):
    user_id = message.from_user.id
    vpn_number = message.text

    await message.answer(
        "Отлично! Сохранил тебя в базе данных!",
        reply_markup=ReplyKeyboardRemove()
    )
    # Обновляем или добавляем запись в базу данных
    cursor.execute("INSERT OR REPLACE INTO users (user_id, vpn_number) VALUES (?, ?)", (user_id, vpn_number))
    conn.commit()


@router.message(F.text.lower() == "нет")
async def answer_no(message: Message):
    await message.answer(
        "Тогда давай еще разок. Напиши первые две цифры своего файлика",
        reply_markup=ReplyKeyboardRemove()
    )
