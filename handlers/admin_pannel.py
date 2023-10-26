import logging

from aiogram.fsm.context import FSMContext

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove

from Forms.admin_pannel_form import Form
from keyboards.keyboards import get_admin_kb, get_yes_no_kb

from db_funcs.db import get_all_users, get_validate_users, set_user_valid

from secret import ADMIN_PASSWORD

form_router = Router()


@form_router.message(Command("admin"))
async def command_admin_panel(message: Message, state: FSMContext) -> None:
    if message.text == f"/admin {ADMIN_PASSWORD}":  # Проверка пароля
        await message.answer(
            "Добро пожаловать в административную панель!",
            reply_markup=get_admin_kb(),
        )
        await state.set_state(Form.start_commands)

    else:
        await message.answer("Неправильный пароль!")


@form_router.message(Form.start_commands, F.text.casefold() == "show_users")
async def process_show_users(message: Message) -> None:
    users = get_all_users()  # возвращает список пользователей из базы данных
    response = "\n".join([f"{user[0]} - {user[1]} - {user[2]} - {user[3]} - {user[4]}" for user in users])
    await message.answer("user_id - user_name - vpn_num - points - valid\n" + response)


@form_router.message(Form.start_commands, F.text.casefold() == "confirm_payment")
async def process_confirm_payment(message: Message, state: FSMContext) -> None:
    users = get_validate_users()  # возвращает список пользователей из базы данных
    response = "\n".join([f"{user[0]} - {user[1]} - {user[2]} - {user[3]} - {user[4]}" for user in users])
    await message.answer("user_id - user_name - vpn_num - points - valid\n" + response)
    await message.answer(
        "Введи впн-номер пользователя, которого надо подтвердить",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.set_state(Form.confirm_payment)


@form_router.message(Form.confirm_payment, F.text.isdigit())
async def process_confirm_payment(message: Message, state: FSMContext) -> None:
    vpn_num = message.text
    await state.update_data(vpn_num=vpn_num)

    await message.reply(
        f"Подтвержаем оплату пользователя с номером {vpn_num}?",
        reply_markup=get_yes_no_kb(),
    )


@form_router.message(Form.confirm_payment, F.text.casefold() == "да")
async def process_confirm_payment_yes(message: Message, state: FSMContext) -> None:

    data = await state.get_data()
    vpn_num = data.get("vpn_num")
    db_answer = set_user_valid(vpn_num)

    if db_answer:
        await message.reply(
            f"Подтверждение прошло успешно!",
            reply_markup=get_admin_kb(),
        )

    else:
        await message.reply(
            f"Пользователя с таким номером не существует или он уже подтвержден",
            reply_markup=get_admin_kb(),
        )

    await message.answer("Напиши номер другого пользователя, кого надо подтвердить или выбери другую команду")


@form_router.message(Form.confirm_payment, F.text.casefold() == "нет")
async def process_confirm_payment_no(message: Message) -> None:

    await message.reply(
        f"Напиши номер человека, которого надо подтвердить",
        reply_markup=ReplyKeyboardRemove(),
    )


@form_router.message(Form.confirm_payment)
async def process_unknown_confirm_payment(message: Message) -> None:
    await message.reply("Я не понимаю тебя :(")

