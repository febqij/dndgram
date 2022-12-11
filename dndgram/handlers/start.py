from aiogram import Router
from aiogram import types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot import dp
from handlers.menu import show_menu
from utils.filters.chat_type import ChatTypeFilter
import utils.db_api.db_quick_commands as db

import middlewares as mdlw

from bot import bot


router_start = Router()
router_start.message(ChatTypeFilter(chat_type=["private"]))
router_start.callback_query.middleware(mdlw.ChatHistoryCallbackQueryMiddleware())
router_start.message.middleware(mdlw.ChatHistoryMessageMiddleware())


@router_start.message(Command("start"))
async def command_start(message: types.Message, state: FSMContext):
    """Регистрация id и username при инициации команды /start"""
    if await db.register_user(message):
        await message.answer(f'Добро пожаловать, {message.from_user.username}!')
    await show_menu(message, state)
