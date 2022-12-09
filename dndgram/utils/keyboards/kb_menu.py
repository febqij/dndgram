from aiogram import types
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


class MenuCallBack(CallbackData, prefix="menu"):
    button: str


def get_kb_menu() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text="Мой профиль",
        callback_data=MenuCallBack(
            button="profile"
        ).pack()
    )
    keyboard.button(
        text="Поиск",
        callback_data=MenuCallBack(
            button="search"
        ).pack()
    )
    keyboard.adjust(2)
    return keyboard.as_markup(resize_keyboard=True)
