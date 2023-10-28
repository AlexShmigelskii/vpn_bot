from essentials import bot


async def send_confirmation(user_id):
    response = 'Оплата была подтверждена. Спасибо :)'
    await bot.send_message(chat_id=user_id, text=response)


async def send_rejection(user_id):
    response = 'Оплата была отвергнута. Вскоре с Вами свяжутся'
    await bot.send_message(chat_id=user_id, text=response)
