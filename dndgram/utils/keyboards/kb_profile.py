from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData


class ProfileCallBack(CallbackData, prefix="profile"):
    button: str


def get_kb_profile() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text="Возраст", callback_data=ProfileCallBack(button="age").pack()
            ),
            InlineKeyboardButton(
                text="Пол", callback_data=ProfileCallBack(button="gender").pack()
            )
        ],
        [
            InlineKeyboardButton(
                text="Ролевая система", callback_data=ProfileCallBack(button="preferences").pack()
            ),
            InlineKeyboardButton(
                text="О себе", callback_data=ProfileCallBack(button="bio").pack()
            )
        ],
        [
            InlineKeyboardButton(
                text="Назад в меню", callback_data=ProfileCallBack(button="back").pack()
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
