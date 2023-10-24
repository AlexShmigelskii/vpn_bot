from aiogram.fsm.context import FSMContext
from Forms.add_vpn_num_form import Form

import logging

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.keyboards import get_yes_no_kb
from db_funcs.db import check_existing_user, write_user_to_db


form_router = Router()


@form_router.message(Command("start"))
async def command_start(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id

    existing_user = check_existing_user(user_id)

    if existing_user:
        user_name = existing_user[1]
        vpn_number = existing_user[2]  # Получаем номер из базы данных
        points = existing_user[3]  # Получаем количество поинтов из базы данных
        await message.answer(f'Привет, {user_name}! Ты уже в нашей базе данных.')
        await message.answer(f'Твой номер: {vpn_number}. Дней до конца подписки: {points}')
        await message.answer('Если хочешь поменять свой номер, напиши команду "/change_num"!')
        await message.answer('Если хочешь продлить подписку, напиши команду "/get_points"!')

    else:
        await state.set_state(Form.name)
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


@form_router.message(Form.name, F.text.isalpha())
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await state.set_state(Form.vpn_num)
    await message.answer(
        f"Nice to meet you, {message.text}!\nTell me your number",
    )


@form_router.message(Form.vpn_num, F.text.isdigit())
async def process_assure_vpn_number(message: Message, state: FSMContext) -> None:
    await state.update_data(vpn_num=message.text)
    await message.reply(
        f"Is {message.text} - your number?",
        reply_markup=get_yes_no_kb(),
    )


@form_router.message(Form.vpn_num, F.text.casefold() == "yes")
async def process_vpn_num_yes(message: Message, state: FSMContext) -> None:

    data = await state.get_data()
    user_id = message.from_user.id
    user_name = data.get('name')
    vpn_number = data.get('new_vpn_num')
    points = 0
    valid = False

    await message.reply(
        f"Cool {data['name']}! Your number is {data['new_vpn_num']}. Writing it into DB!",
        reply_markup=ReplyKeyboardRemove(),
    )
    write_user_to_db(user_id, user_name, vpn_number, points, valid)
    await state.clear()


@form_router.message(Form.vpn_num, F.text.casefold() == "no")
async def process_vpn_num_no(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    await message.answer(
        f"That's all right {data['name']}! Tell me your true number",
    )


@form_router.message(Form.vpn_num)
async def process_unknown_vpn_num(message: Message) -> None:
    await message.reply("I don't understand you :(")


@form_router.message(Form.name)
async def process_unknown_name(message: Message) -> None:
    await message.reply("Don't try to fool me!")
