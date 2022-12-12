from typing import List

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData

from data.config import logger


class PreferencesCallBack(CallbackData, prefix="preferences"):
    button: str


PREFERENCES_CHOICES = [
    ["D&D/5e", "D&D/3.5", "GURPS"]
]


def get_kb_preferences() -> InlineKeyboardMarkup:
    factory_button = [
        [InlineKeyboardButton(
            text=value,
            callback_data=PreferencesCallBack(button=value).pack()
        ) for value in x] for x in PREFERENCES_CHOICES
    ]
    back_button = [
        [
            InlineKeyboardButton(
                text="Назад в профиль",
                callback_data=PreferencesCallBack(button="back").pack()
            )
        ]
    ]
    buttons = factory_button + back_button
    return InlineKeyboardMarkup(inline_keyboard=buttons)
