from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from funcs.db import get_user_info


form_router = Router()


@form_router.message(Command("show_profile"))
async def process_show_profile(message: Message) -> None:
    user_id = message.from_user.id  # Получаем ID пользователя, который отправил команду
    user_info = get_user_info(user_id)

    if user_info:
        user_id, user_name, vpn_number, points, valid, on_validation, notifications = user_info
        response = (f"Имя пользователя: {user_name}"
                    f"\nVPN номер: {vpn_number}"
                    f"\nДней подписки: {points}"
                    f"\nСтатус: {'Ждет валидации' if valid else 'Можно пополнять'}"
                    f"\nОжидающие подтверждение: {on_validation} дней"
                    f"\nУведомления от бота {'включены' if notifications else 'выключены'}")
        await message.answer(response)
    else:
        await message.answer("Кажется, вы не зарегистрированы в системе или ваш профиль не найден.")

