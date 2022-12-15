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


router_location = Router()
router_location.message(ChatTypeFilter(chat_type=["private"]))
router_location.callback_query.middleware(mdlw.ChatHistoryCallbackQueryMiddleware())
router_location.message.middleware(mdlw.ChatHistoryMessageMiddleware())


def get_location_text(user: User):
    if user.location:
        return (
            f"{html.bold('У вас указано следующее местоположение:')}\n"
            f"{user.location}"
        )
    return (
        "В данной графе пусто. Вы можете изменить отображаемое местоположение, "
        "отправив сообщением наименование города."
    )


def location_keyboard_select(location: str):
    """
    Returns the keyboard variation depending on whether the location is filled in
    or not.
    """
    return kb.get_kb_location_full() if location else kb.get_kb_location_short()


@router_location.callback_query(kb.ProfileCallBack.filter(F.button == "location"))
async def edit_location_callback(callbackquery: types.CallbackQuery, state: FSMContext):
    await state.set_state(UserState.location)

    message: types.Message = callbackquery.message
    user: User = await dbqc.select_user(callbackquery.from_user.id)

    sended_message: types.Message = await bot.send_message(
        text="Или воспользуйтесь функцией геолокации с помощью кнопки ниже.",
        chat_id=callbackquery.from_user.id,
        reply_markup=kb.get_ckb_location()
    )

    if not await dbqc.select_message(sended_message.message_id):
        await dbqc.insert_message_id(sended_message)

    with suppress(TelegramBadRequest):
        await message.edit_text(
            text=get_location_text(user),
            reply_markup=location_keyboard_select(user.location)
        )


@router_location.message(Command("location"))
async def edit_location_command(
    message: types.Message,
    state: FSMContext
):
    await state.set_state(UserState.location)

    user: User = await dbqc.select_user(message.from_user.id)

    await message.answer(
            text=get_location_text(user),
            reply_markup=location_keyboard_select(user.location)
        )


