from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardMarkup, KeyboardButton
)
from aiogram.filters.callback_data import CallbackData


class LocationCallBack(CallbackData, prefix="location"):
    button: str


def get_kb_location_full() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text="Очистить данные",
                callback_data=LocationCallBack(button="reset_location").pack()
            ),
        ],
        [
            InlineKeyboardButton(
                text="Назад в профиль",
                callback_data=LocationCallBack(button="back").pack()
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_kb_location_short() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text="Назад в профиль",
                callback_data=LocationCallBack(button="back").pack()
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_ckb_location() -> ReplyKeyboardMarkup:
    keyboard = [
        [
            KeyboardButton(text="Геолокация", request_location=True)   
        ]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
