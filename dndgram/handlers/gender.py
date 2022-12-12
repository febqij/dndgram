from contextlib import suppress

from aiogram.filters import Command
from aiogram import Router, types, html, F
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

import utils.db_api.db_quick_commands as dbqc
from utils.filters.chat_type import ChatTypeFilter
import utils.keyboards as kb
from utils.state import UserState
from utils.db_api.schemas import User, Chat
import middlewares as mdlw

from data.config import logger

from bot import bot


router_gender = Router()
router_gender.message(ChatTypeFilter(chat_type=["private"]))
router_gender.callback_query.middleware(mdlw.ChatHistoryCallbackQueryMiddleware())
router_gender.message.middleware(mdlw.ChatHistoryMessageMiddleware())


def get_gender_text(user: User):
    if user.gender:
        return (f"Ваш указанный текущий пол: {html.code(user.gender)}")
    return (
        "Данные о вашем поле отсутствуют.\n"
        "Чтобы изменить значение нажмите на соответствующую кнопку ниже:"
    )


def gender_keyboard_select(gender: str):
    """
    Returns the keyboard variation depending on whether the gender is filled in
    or not.
    """
    return kb.get_kb_gender_full() if gender else kb.get_kb_gender_short()


def gender_decoder(gender: str):
    if gender == "male":
        return "🙎🏼‍♂️"
    if gender == "female":
        return "🙍🏼‍♀️"
    if gender == "🙎🏼‍♂️":
        return "male"
    if gender == "🙍🏼‍♀️":
        return "female"


@router_gender.callback_query(
    kb.ProfileCallBack.filter(F.button == "gender")
)
async def edit_gender_callback(callbackquery: types.CallbackQuery, state: FSMContext):
    await state.set_state(UserState.gender)
    message: types.Message = callbackquery.message
    user: User = await dbqc.select_user(callbackquery.from_user.id)

    with suppress(TelegramBadRequest):
        await message.edit_text(
            text=get_gender_text(user),
            reply_markup=gender_keyboard_select(user.gender)
        )


@router_gender.message(Command("gender"))
async def edit_gender_command(
    message: types.Message,
    state: FSMContext
):
    await state.set_state(UserState.gender)

    user: User = await dbqc.select_user(message.from_user.id)

    await message.answer(
            text=get_gender_text(user),
            reply_markup=gender_keyboard_select(user.age)
        )


@router_gender.callback_query(
    kb.GenderCallBack.filter(F.button.in_({"male", "female"}))
)
async def choose_gender_value(
    callbackquery: types.CallbackQuery,
    state: FSMContext
):
    user: User = await dbqc.get_last_bot_message(callbackquery.from_user.id)
    chat: Chat = list(user.chat)[0]

    try:
        gender = await dbqc.insert_gender(callbackquery)
        await callbackquery.answer(
            text=f"Изменено на {gender_decoder(gender)}"
        )
    except Exception as e:
        await callbackquery.answer(
                text="Что-то пошло не так 🤷‍♂️"
            )
        logger.error(
            "An unexpected error has occurred in the handlers/gender.py "
            f"choose_gender_value while trying insert_gender:\n{e}"
        )
    finally:
        await edit_gender_callback(callbackquery, state)


@router_gender.message(UserState.gender, F.content_type.in_({'text'}))
async def entering_gender_value(
    message: types.Message,
    state: FSMContext
):
    user: User = await dbqc.get_last_bot_message(message.from_user.id)
    chat: Chat = list(user.chat)[0]

    text = "Пожалуйста, воспользуйтесь кнопками вместо ввода текста:"

    with suppress(TelegramBadRequest):
        await bot.edit_message_text(
            text=text,
            chat_id=message.from_user.id,
            message_id=chat.message_id,
            reply_markup=gender_keyboard_select(user.age)
        )


@router_gender.callback_query(
    kb.GenderCallBack.filter(F.button == "reset_gender")
)
async def reset_gender_callback(
    callbackquery: types.CallbackQuery, state: FSMContext
):
    user: types.User = callbackquery.from_user

    if await dbqc.delete_gender(user):
        await edit_gender_callback(callbackquery, state)
        await callbackquery.answer(
                text="Данные о половой принадлежности удалены из вашего профиля."
            )
