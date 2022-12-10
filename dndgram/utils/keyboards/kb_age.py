from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData


class AgeCallBack(CallbackData, prefix="age"):
    button: str


def get_kb_age() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text="Убрать возраст", callback_data=AgeCallBack(button="reset_age").pack()
            ),
        ],
        [
            InlineKeyboardButton(
                text="Назад в профиль", callback_data=AgeCallBack(button="back").pack()
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
