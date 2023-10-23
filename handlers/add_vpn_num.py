from aiogram.fsm.context import FSMContext
from Forms.start_form import StartForm

import logging

import sqlite3
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.for_validate import get_yes_no_kb


form_router = Router()

# Подключение к базе данных
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Создание таблицы пользователей (id, номер телефона и количество поинтов)
cursor.execute('''CREATE TABLE IF NOT EXISTS users
                  (user_id INTEGER PRIMARY KEY, vpn_number INT, points INT)''')
conn.commit()


@form_router.message(Command("start"))
async def command_start(message: Message, state: FSMContext) -> None:
    await state.set_state(StartForm.name)
    await message.answer(
        "Hi there! What's your name?",
        reply_markup=ReplyKeyboardRemove(),
    )


@form_router.message(Command("cancel"))
@form_router.message(F.text.casefold() == "cancel")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info("Cancelling state %r", current_state)
    await state.clear()
    await message.answer(
        "Cancelled.",
        reply_markup=ReplyKeyboardRemove(),
    )


@form_router.message(StartForm.name)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await state.set_state(StartForm.vpn_num)
    await state.set_state(StartForm.vpn_num)
    await message.answer(
        f"Nice to meet you, {message.text}!\nTell me your number",
    )


@form_router.message(StartForm.vpn_num, F.text.isdigit())
async def process_assure_vpn_number(message: Message, state: FSMContext) -> None:
    await state.update_data(vpn_num=message.text)
    await message.reply(
        f"Is {message.text} - your number?",
        reply_markup=get_yes_no_kb(),
    )


@form_router.message(StartForm.vpn_num, F.text.casefold() == "yes")
async def process_vpn_num_yes(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    await message.reply(
        f"Cool {data['name']}! Your number is {data['vpn_num']}. Writing it into DB!",
        reply_markup=ReplyKeyboardRemove(),
    )


@form_router.message(StartForm.vpn_num, F.text.casefold() == "no")
async def process_vpn_num_no(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    await message.answer(
        f"That's all right {data['name']}! Tell me your true number",
    )


@form_router.message(StartForm.vpn_num)
async def process_unknown_vpn_num(message: Message) -> None:
    await message.reply("I don't understand you :(")

