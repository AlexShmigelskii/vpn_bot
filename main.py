import asyncio
from aiogram import Bot, Dispatcher

import logging
import sys

import secret
from handlers import questions, different_types, points, add_vpn_num


# Запуск бота
async def main():
    bot = Bot(token=secret.TOKEN)
    dp = Dispatcher()

    dp.include_routers(add_vpn_num.form_router)

    # Альтернативный вариант регистрации роутеров по одному на строку
    # dp.include_router(questions.router)
    # dp.include_router(different_types.router)

    # Запускаем бота и пропускаем все накопленные входящие
    # Да, этот метод можно вызвать даже если у вас поллинг
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
