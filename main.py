import asyncio
from aiogram import Bot, Dispatcher
import schedule

import logging
import sys

import secret
from db_funcs.db import create_database, decrease_points
from handlers import add_vpn_num, get_points, different_types, change_vpn_num, admin_pannel

bot = Bot(token=secret.TOKEN)
dp = Dispatcher()

schedule.every(1).minutes.do(decrease_points)


async def run_schedule():
    while True:
        await asyncio.sleep(1)  # Ждем 1 секунду
        schedule.run_pending()


# Запуск бота
async def main():
    dp.include_routers(
        add_vpn_num.form_router,
        get_points.form_router,
        change_vpn_num.form_router,
        admin_pannel.form_router,
        different_types.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    create_database()
    loop = asyncio.get_event_loop()
    loop.create_task(run_schedule())  # Создаем задачу для цикла асинхронного выполнения
    loop.create_task(main())  # Создаем задачу для функции main()
    loop.run_forever()  # Запускаем цикл асинхронного выполнения
