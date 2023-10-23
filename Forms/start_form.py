from aiogram.fsm.state import StatesGroup, State


class StartForm(StatesGroup):
    name = State()
    vpn_num = State()
