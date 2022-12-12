from typing import List

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData


class GenderCallBack(CallbackData, prefix="gender"):
    button: str


CHOOSE_GENDER: List[InlineKeyboardButton] = [
            InlineKeyboardButton(
                text="🙎🏼‍♂️",
                callback_data=GenderCallBack(button="male").pack()
            ),
            InlineKeyboardButton(
                text="🙍🏼‍♀️",
                callback_data=GenderCallBack(button="female").pack()
            ),
        ]


def get_kb_gender_full() -> InlineKeyboardMarkup:
    buttons = [
        CHOOSE_GENDER,
        [
            InlineKeyboardButton(
                text="Убрать пол",
                callback_data=GenderCallBack(button="reset_gender").pack()
            ),
        ],
        [
            InlineKeyboardButton(
                text="Назад в профиль",
                callback_data=GenderCallBack(button="back").pack()
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_kb_gender_short() -> InlineKeyboardMarkup:
    buttons = [
        CHOOSE_GENDER,
        [
            InlineKeyboardButton(
                text="Назад в профиль",
                callback_data=GenderCallBack(button="back").pack()
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
