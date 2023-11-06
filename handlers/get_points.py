import logging

from aiogram.fsm.context import FSMContext

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove

from Forms.get_points_form import Form
from keyboards.keyboards import get_yes_no_kb, get_duration_kb

from funcs.db import check_existing_user, update_user_points, check_need_validation
from secret import CARD_NUM

form_router = Router()


@form_router.message(Command("get_points"))
async def command_get_points(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id

    existing_user = check_existing_user(user_id)

    if existing_user:

        if check_need_validation(user_id):

            await message.answer(
                f"Прости,я еще не успел проверить твое старое пополнение!",
                reply_markup=ReplyKeyboardRemove(),
            )
            await state.clear()

        else:

            user_name = existing_user[1]
            vpn_number = existing_user[2]  # Получаем номер из базы данных
            points = existing_user[3]  # Получаем количество поинтов из базы данных

            await message.answer(f'{user_name} ({vpn_number}), у тебя еще {points} дней подписки!')
            await message.answer(
                'Хочешь продлить подписку?',
                reply_markup=get_yes_no_kb()
            )
            await state.set_state(Form.want_to_purchase)

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


@form_router.message(Form.want_to_purchase, F.text.casefold() == "да")
async def process_want_to_purchase_yes(message: Message, state: FSMContext) -> None:

    await message.reply(
        f"Отлично! На сколько дней ты хочешь продлить подписку?",
        reply_markup=get_duration_kb(),
    )
    await state.set_state(Form.select_duration)


@form_router.message(Form.want_to_purchase, F.text.casefold() == "нет")
async def process_want_to_purchase_no(message: Message, state: FSMContext) -> None:

    await message.reply(
        f"Это печально(",
        reply_markup=ReplyKeyboardRemove(),
    )
    await message.answer_sticker('CAACAgIAAxkBAAEKlbtlNs1hWQIfElCygR6Wv9hITQPHGwACfhoAAmZWIEpJ207LaLOGJzAE')
    await state.clear()


@form_router.message(Form.want_to_purchase)
async def process_unknown_want_to_purchase(message: Message) -> None:
    await message.reply("Я не понимаю тебя :(")


@form_router.message(Form.select_duration, F.text.in_({'30', '60'}))
async def process_duration(message: Message, state: FSMContext) -> None:

    days = message.text
    await state.update_data(duration=days)

    await message.reply(
        f"Ты выбрал {days} дней",
        reply_markup=get_yes_no_kb(),
    )


@form_router.message(Form.select_duration, F.text.casefold() == "да")
async def process_duration_yes(message: Message, state: FSMContext) -> None:

    data = await state.get_data()
    duration = data.get("duration")

    await message.reply(
        f"Хорошо. Вот мои реквизиты"
        f"\nНомер карты: {CARD_NUM} - Александр Ш."
        f"\nСумма: {int(duration) / 30 * 50}р",
        reply_markup=ReplyKeyboardRemove(),
    )
    await message.answer(
        "После оплаты пришли скриншот в чат"
        "\nПринимаю только одну фотографию"
    )
    await state.set_state(Form.send_photo)


@form_router.message(Form.select_duration, F.text.casefold() == "нет")
async def process_duration_no(message: Message) -> None:

    await message.reply(
        f"Выбор за тобой",
        reply_markup=get_duration_kb(),
    )


@form_router.message(Form.select_duration)
async def process_unknown_duration(message: Message) -> None:
    await message.reply("Я не понимаю тебя :(")


@form_router.message(Form.send_photo, F.photo)
async def process_send_photo(message: Message, state: FSMContext) -> None:

    from essentials import bot
    user_id = message.from_user.id
    user = check_existing_user(user_id)
    admin_id = 1298017336
    photo = message.photo[-1].file_id
    data = await state.get_data()
    duration = data.get("duration")

    await bot.send_photo(chat_id=admin_id, photo=photo, caption=f'Новый перевод:\n'
                                                                f'от {user[1]} ({user[2]})\n'
                                                                f'на {duration} дней')
    db_response = update_user_points(user_id, duration)

    if db_response:
        await message.reply(
            f"Фотографию получил. Подписка будет продлена на {duration} дней после проверки!",
            reply_markup=ReplyKeyboardRemove(),
        )
    else:
        await message.reply(
            f"Тебе нужно дождаться, пока я проверю предыдущую фотографию",
            reply_markup=ReplyKeyboardRemove(),
        )
    await state.clear()


@form_router.message(Form.send_photo)
async def process_unknown_send_photo(message: Message) -> None:
    await message.reply("На данном этапе я принимаю только фотографии")
