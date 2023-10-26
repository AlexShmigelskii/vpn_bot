from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_yes_no_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Да")
    kb.button(text="Нет")
    kb.button(text="cancel")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)


def get_duration_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="30")
    kb.button(text="60")
    kb.button(text="90")
    kb.button(text="cancel")
    kb.adjust(3)
    return kb.as_markup(resize_keyboard=True)


def get_command_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="/start")
    kb.button(text="/get_points")
    kb.button(text="/change_num")
    kb.adjust(3)
    return kb.as_markup(resize_keyboard=True)


def get_admin_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="show_users")
    kb.button(text="confirm_payment")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)
