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


router_age = Router()
router_age.message(ChatTypeFilter(chat_type=["private"]))
router_age.callback_query.middleware(mdlw.ChatHistoryCallbackQueryMiddleware())
router_age.message.middleware(mdlw.ChatHistoryMessageMiddleware())



def get_age_text(user: User):
    if user.age:
        return (f"Ваш указанный текущий возраст: {html.code(user.age)}")
    return (
        "Данные о вашем возрасте отсутствуют.\n"
        "Чтобы изменить значение отправьте в данный диалог сообщение в виде целого числа."
    )


def age_keyboard_select(age: int):
    """
    Returns the keyboard variation depending on whether the age is filled in
    or not.
    """
    return kb.get_kb_age_full() if age else kb.get_kb_age_short()


@router_age.callback_query(
    kb.ProfileCallBack.filter(F.button == "age")
)
async def edit_age_callback(callbackquery: types.CallbackQuery, state: FSMContext):
    await state.set_state(UserState.age)

    message: types.Message = callbackquery.message
    user: User = await dbqc.select_user(callbackquery.from_user.id)

    with suppress(TelegramBadRequest):
        await message.edit_text(
            text=get_age_text(user),
            reply_markup=age_keyboard_select(user.age)
        )


@router_age.message(Command("age"))
async def edit_age_command(
    message: types.Message,
    state: FSMContext
):
    await state.set_state(UserState.age)

    user: User = await dbqc.select_user(message.from_user.id)

    await message.answer(
            text=get_age_text(user),
            reply_markup=age_keyboard_select(user.age)
        )


@router_age.message(UserState.age, F.content_type.in_({'text'}))
async def entering_age_value(
    message: types.Message,
    state: FSMContext
):
    user: User = await dbqc.get_last_bot_message(message.from_user.id)
    chat: Chat = list(user.chat)[0]

    try:
        age = int(message.text)
        if age < 13:
            text = "Слишком маленькое значение:"
        if age > 70:
            text = "Попробуйте еще раз, на этот раз без шуток:"
        else:
            age = await dbqc.insert_age(message)
            text = f"Ваш возраст успешно изменен на {age}"
    except ValueError:
        text = "Введите корректный возраст в виде целочисленного значения:"
    finally:
        await bot.edit_message_text(
            text=text,
            chat_id=message.from_user.id,
            message_id=chat.message_id,
            reply_markup=age_keyboard_select(user.age)
        )


@router_age.callback_query(
    kb.AgeCallBack.filter(F.button == "reset_age")
)
async def reset_age_callback(callbackquery: types.CallbackQuery, state: FSMContext):
    user: types.User = callbackquery.from_user

    if await dbqc.delete_age(user):
        await edit_age_callback(callbackquery, state)
        await callbackquery.answer(
                text="Данные о возрасте удалены из вашего профиля."
            )
