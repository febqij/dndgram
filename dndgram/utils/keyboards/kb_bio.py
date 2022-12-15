from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData


class BioCallBack(CallbackData, prefix="bio"):
    button: str


def get_kb_bio_full() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text="Очистить данные", callback_data=BioCallBack(button="reset_bio").pack()
            ),
        ],
        [
            InlineKeyboardButton(
                text="Назад в профиль", callback_data=BioCallBack(button="back").pack()
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_kb_bio_short() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text="Назад в профиль", callback_data=BioCallBack(button="back").pack()
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
