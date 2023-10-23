from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    want_to_purchase = State()
    select_duration = State()
    send_photo = State()
    validation = State()
