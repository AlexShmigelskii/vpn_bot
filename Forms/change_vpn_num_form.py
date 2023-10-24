from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    validate = State()
    new_vpn_num = State()
