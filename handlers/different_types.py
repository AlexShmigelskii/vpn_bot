from aiogram import Router, F
from aiogram.types import Message

import random

router = Router()

STICKERS = ['CAACAgIAAxkBAAEKkJFlMuxRNXvaKC6CV5AVAhnjvBVtcgACIQgAAvaWIEoXKn6oDdX25DAE',
            'CAACAgIAAxkBAAEKkJZlMuz00MmUO4f5ApuCdazCv2RsdwACIC4AAr3I4Uu0jRzVoxnItDAE',
            'CAACAgIAAxkBAAEKkJhlMu0H9j-UrucqzE8GQDL5F0zQOAACwRQAAkUrWEicagVRWPL21zAE']


# @router.message(F.text)
# async def message_with_text(message: Message):
#     await message.answer_sticker(random.choice(STICKERS))
#
#
# @router.message(F.sticker)
# async def message_with_sticker(message: Message):
#     await message.answer_sticker(random.choice(STICKERS))
#
#
# @router.message(F.animation)
# async def message_with_gif(message: Message):
#     await message.answer_sticker(random.choice(STICKERS))
