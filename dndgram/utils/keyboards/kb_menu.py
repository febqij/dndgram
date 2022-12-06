from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_kb_menu() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Мой профиль", callback_data="profile")
    keyboard.button(text="Поиск", callback_data="search")
    keyboard.adjust(2)
    return keyboard.as_markup(resize_keyboard=True)
