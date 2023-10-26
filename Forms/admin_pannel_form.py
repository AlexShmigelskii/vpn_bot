from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    start_commands = State()
    confirm_payment = State()
    reject_payment = State()
    validate = State()
