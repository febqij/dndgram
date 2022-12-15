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


router_bio = Router()
router_bio.message(ChatTypeFilter(chat_type=["private"]))
router_bio.callback_query.middleware(mdlw.ChatHistoryCallbackQueryMiddleware())
router_bio.message.middleware(mdlw.ChatHistoryMessageMiddleware())


def get_bio_text(user: User):
    if user.bio:
        return (
            f"{html.bold('Ваше текущее описание:')}\n"
            f"{user.bio}"
        )
    return (
        "В данной графе пусто. Вы можете изменить содержимое, отправив текст "
        "в сообщении ниже:"
    )


def bio_keyboard_select(bio: str):
    """
    Returns the keyboard variation depending on whether the bio is filled in
    or not.
    """
    return kb.get_kb_bio_full() if bio else kb.get_kb_bio_short()


@router_bio.callback_query(kb.ProfileCallBack.filter(F.button == "bio"))
async def edit_bio_callback(callbackquery: types.CallbackQuery, state: FSMContext):
    await state.set_state(UserState.bio)

    message: types.Message = callbackquery.message
    user: User = await dbqc.select_user(callbackquery.from_user.id)

    with suppress(TelegramBadRequest):
        await message.edit_text(
            text=get_bio_text(user),
            reply_markup=bio_keyboard_select(user.bio)
        )


@router_bio.message(Command("bio"))
async def edit_bio_command(
    message: types.Message,
    state: FSMContext
):
    await state.set_state(UserState.bio)

    user: User = await dbqc.select_user(message.from_user.id)

    await message.answer(
            text=get_bio_text(user),
            reply_markup=bio_keyboard_select(user.bio)
        )


@router_bio.message(UserState.bio, F.content_type.in_({'text'}))
async def entering_bio_value(
    message: types.Message,
    state: FSMContext
):
    user: User = await dbqc.get_last_bot_message(message.from_user.id)
    chat: Chat = list(user.chat)[0]

    try:
        await dbqc.update_bio(message)
        text = (
            f"{html.bold('Текст описания обновлен:')}\n"
            f"{message.text}"
        )
    except ValueError as e:
        text = "Что-то пошло не так, пожалуйста, сообщите об этом владельцу:"
        logger.error(e.__traceback__)
    finally:
        await bot.edit_message_text(
            text=text,
            chat_id=message.from_user.id,
            message_id=chat.message_id,
            reply_markup=bio_keyboard_select(user.bio)
        )


@router_bio.callback_query(
    kb.BioCallBack.filter(F.button == "reset_bio")
)
async def reset_bio_callback(callbackquery: types.CallbackQuery, state: FSMContext):
    user: types.User = callbackquery.from_user

    if await dbqc.clear_bio(user.id):
        await edit_bio_callback(callbackquery, state)
        await callbackquery.answer(
                text="Текущие данные были удалены из вашего профиля."
            )
