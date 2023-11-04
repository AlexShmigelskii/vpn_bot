from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from funcs.db import toggle_subscription_notification

form_router = Router()


@form_router.message(Command("toggle_notifications"))
async def process_toggle_notifications(message: Message) -> None:
    user_id = message.from_user.id  # Получаем ID пользователя, который отправил команду
    notification_status = toggle_subscription_notification(user_id)

    if notification_status:

        await message.answer(text=f"Уведомления {'включены' if notification_status else 'выключены'}!")

    else:
        await message.answer(text="Тебя нет в моей базе данных! Для начала нажми команду /start")
