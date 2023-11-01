import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from essentials import bot
from funcs.db import check_subscription_expiry, decrease_points

scheduler = AsyncIOScheduler()


async def send_expire_notification():
    users_to_notify = check_subscription_expiry()

    for user in users_to_notify:
        user_id = user[0]
        user_points = user[1]
        await bot.send_message(chat_id=user_id,
                               text=f"Ваша подписка истекает. Пожалуйста, пополните ее!"
                                    f"\nОсталось дней:{user_points}",
                               disable_notification=True)


async def run_schedule():
    # Планируем выполнение decrease_points каждую минуту
    scheduler.add_job(decrease_points, 'interval', minutes=1)

    # Планируем выполнение send_expire_notification каждую минуту
    scheduler.add_job(send_expire_notification, 'interval', minutes=1)

    # Запускаем планировщик
    scheduler.start()
