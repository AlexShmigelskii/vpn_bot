import sqlite3
from aiogram.types import Message
from aiogram import Router, F

router = Router()

# Подключение к базе данных
conn = sqlite3.connect('users.db')
cursor = conn.cursor()


@router.message(F.text.lower() == "/points")
async def cmd_get_points(message: Message):
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
        await message.answer('Тут ты можешь пополнить свои поинты!')

    else:
        await message.answer(f'Тебя нет в моей базе данных!')
        await message.answer(f'Для начала введи команду "/start" и введи свой номер')

