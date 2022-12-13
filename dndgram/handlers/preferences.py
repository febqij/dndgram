from contextlib import suppress
from typing import List, Set

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


router_preferences = Router()
router_preferences.message(ChatTypeFilter(chat_type=["private"]))
router_preferences.callback_query.middleware(mdlw.ChatHistoryCallbackQueryMiddleware())
router_preferences.message.middleware(mdlw.ChatHistoryMessageMiddleware())


def get_preference_text(user: User):
    if user.preferences:
        return (f"Ваш текущий список предпочитаемых игровых систем: {html.code(user.preferences)}")
    return (
        "Данные о ваших игровых предпочтениях отсутствуют.\n"
        "Чтобы добавить или убрать элемент из списка предпочтений нажмите на соответствующую кнопку:"
    )


@router_preferences.callback_query(
    kb.ProfileCallBack.filter(F.button == "preferences")
)
async def edit_preferences_callback(callbackquery: types.CallbackQuery, state: FSMContext):
    await state.set_state(UserState.preferences)
    message: types.Message = callbackquery.message
    user: User = await dbqc.select_user(callbackquery.from_user.id)

    with suppress(TelegramBadRequest):
        await message.edit_text(
            text=get_preference_text(user),
            reply_markup=kb.get_kb_preferences()
        )


@router_preferences.message(Command("preferences"))
async def edit_preference_command(
    message: types.Message,
    state: FSMContext
):
    await state.set_state(UserState.preferences)

    user: User = await dbqc.select_user(message.from_user.id)

    await message.answer(
            text=get_preference_text(user),
            reply_markup=kb.get_kb_preferences()
        )


def union_preferences():
    """Converting a list of lists into a single set for a magic filter."""
    _list = []

    for i in kb.PREFERENCES_CHOICES:
        _list.extend(iter(i))

    return set(_list)


async def get_set_preferences(user_id: int):
    preferences = await dbqc.get_preferences(user_id)

    if preferences is None:
        preferences: Set = set()
        length = 0
    else:
        preferences: Set = set(preferences.split(","))
        length = len(preferences)
    logger.debug(f"length, preferences: {length}, {preferences}")
    return length, preferences

@router_preferences.callback_query(
    kb.PreferencesCallBack.filter(F.button.in_(union_preferences()))
)
async def choose_preferences_value(
    callbackquery: types.CallbackQuery,
    state: FSMContext
):
    try:
        user_id = callbackquery.from_user.id
        length, preferences = await get_set_preferences(user_id)
        pending_value: str = (callbackquery.data).split(":")[1]
        if pending_value not in preferences:
            preferences.add(pending_value)
            preferences = ",".join(preferences)
            await dbqc.insert_preference(preferences, user_id)
            await callbackquery.answer(
                text=f"{pending_value} добавлена в ваш список."
            )

        elif length > 1:
            preferences.remove(pending_value)
            preferences = ",".join(preferences)
            await dbqc.delete_preference(preferences, user_id)
            await callbackquery.answer(
                text=f"{pending_value} убрана из списка ваших предпочтений."
            )
        else:
            await dbqc.clear_preferences(user_id)
            await callbackquery.answer(
                text=(
                    f"{pending_value} убрана из списка ваших предпочтений.\n"
                    "Список теперь пуст"
                )
            )

    except Exception as e:
        await callbackquery.answer(
                text="Что-то пошло не так 🤷‍♂️"
            )
        logger.error(
            "An unexpected error has occurred in the handlers/preferences.py "
            f"`choose_preferences_value` previously unhandled error:\n{e}"
        )
    finally:
        await edit_preferences_callback(callbackquery, state)


@router_preferences.message(UserState.preferences, F.content_type.in_({'text'}))
async def entering_preference_value(
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
            reply_markup=kb.get_kb_preferences()
        )
