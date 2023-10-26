from aiogram.fsm.context import FSMContext
from Forms.change_vpn_num_form import Form

import logging

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.keyboards import get_yes_no_kb
from db_funcs.db import check_existing_user, update_user_vpn_num


form_router = Router()


@form_router.message(Command("change_num"))
async def command_change_num(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id

    existing_user = check_existing_user(user_id)

    if existing_user:
        vpn_number = existing_user[2]  # Получаем номер из базы данных
        await message.answer(f'В настоящий момент твой номер - {vpn_number}')
        await message.answer(
            f'Хочешь поменять его?',
            reply_markup=get_yes_no_kb(),
        )
        await state.set_state(Form.validate)

    else:
        await message.answer(
            'Тебя нет в моей базе данных! \nДля начала нажми /start',
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


@form_router.message(Form.validate, F.text.casefold() == "да")
async def process_validate_yes(message: Message, state: FSMContext) -> None:

    await message.reply(
        f"Супер! Назови свой новый номер",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.set_state(Form.new_vpn_num)


@form_router.message(Form.validate, F.text.casefold() == "нет")
async def process_validate_no(message: Message, state: FSMContext) -> None:

    await message.reply(
        f"До встречи!",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.clear()


@form_router.message(Form.validate)
async def process_unknown_validate(message: Message) -> None:
    await message.reply("Я не понимаю тебя :(")


@form_router.message(Form.new_vpn_num, F.text.isdigit())
async def process_new_vpn_num(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    vpn_num = message.text
    db_reply = update_user_vpn_num(user_id, vpn_num)

    await message.reply(
        f"{db_reply}",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.clear()


@form_router.message(Form.new_vpn_num)
async def process_unknown_new_vpn_num(message: Message) -> None:
    await message.reply("Я не понимаю тебя :(")
