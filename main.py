import asyncio
from aiogram import Bot, Dispatcher

import logging
import sys

import secret
from essentials import dp, bot
from funcs.db import create_database
from handlers import add_vpn_num, get_points, different_types, change_vpn_num, admin_pannel, user_info, bot_notifications
from funcs.schedules import run_schedule  # Импортируем асинхронную функцию запуска планировщика


# Запуск бота
async def main():
    dp.include_routers(
        add_vpn_num.form_router,
        get_points.form_router,
        change_vpn_num.form_router,
        admin_pannel.form_router,
        user_info.form_router,
        bot_notifications.form_router,
        different_types.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


# Создаем цикл событий asyncio
async def run():
    await asyncio.gather(main(), run_schedule())  # Запускаем бота и планировщик задач

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    create_database()
    asyncio.run(run())  # Запускаем обе задачи в цикле событий asyncio
