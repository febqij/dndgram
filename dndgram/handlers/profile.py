from aiogram import Router
from aiogram import types
from aiogram.filters import Command
from aiogram import F
from aiogram import html
from aiogram.fsm.context import FSMContext

import utils.db_api.db_quick_commands as db
from utils.filters.chat_type import ChatTypeFilter
import utils.db_api.db_quick_commands as dbqc
import utils.keyboards as kb
from utils.state import UserState
from utils.db_api.schemas import User, Chat

import middlewares as mdlw

from bot import bot
from data.config import logger


router_profile = Router()
router_profile.message(ChatTypeFilter(chat_type=["private"]))
router_profile.callback_query.middleware(mdlw.ChatHistoryCallbackQueryMiddleware())
router_profile.message.middleware(mdlw.ChatHistoryMessageMiddleware())


def get_profile_text(user: User):
    return (
            f"{html.bold('Ваш профиль:')}\n"
            f"Username: {(html.code(f'@{user.username}'))}\n"
            f"Возраст: {html.code(user.age)}\n"
            f"Пол: {html.code(user.gender)}\n"
            f"Ролевая система: {html.code(user.preferences)}\n"
            f"О себе:\n- {html.italic(user.bio)}\n"
        )


@router_profile.callback_query(
    kb.MenuCallBack.filter(F.button == "profile")
)
async def show_profile_callback(callbackquery: types.CallbackQuery, state: FSMContext):
    await state.set_state(UserState.profile)

    message: types.Message = callbackquery.message
    user: User = await db.select_user(callbackquery.from_user.id)

    last_message: Chat = await db.get_last_user_message(user.id)
    logger.debug(
        f"Сообщение с которого выполнен запрос: {message.message_id}\n"
        f"Последнее сообщения с БД: {last_message.message_id}"
        )
    await message.edit_text(
        text=get_profile_text(user),
        reply_markup=kb.get_kb_profile()
    )


@router_profile.message(Command("profile"))
async def show_profile_command(
    message: types.Message,
    state: FSMContext
):
    await state.set_state(UserState.profile)

    user: User = await db.select_user(message.from_user.id)

    await message.answer(
            text=get_profile_text(user),
            reply_markup=kb.get_kb_profile()
        )
