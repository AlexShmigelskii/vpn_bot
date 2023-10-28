import asyncio
import schedule

from essentials import bot
from funcs.db import check_subscription_expiry
from funcs.db import decrease_points


async def send_expire_notification():

    users_to_notify = check_subscription_expiry()

    for user_id in users_to_notify:
        await bot.send_message(chat_id=user_id,
                               text="Ваша подписка истекает. Пожалуйста, пополните ее!",
                               disable_notification=True)


schedule.every(1).minutes.do(decrease_points)
schedule.every().day.at("09:00").do(send_expire_notification)


async def run_schedule():
    while True:
        await asyncio.sleep(1)
        schedule.run_pending()
