from aiogram import types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot import dp
from handlers.menu import show_menu
from utils.filters.chat_type import ChatTypeFilter
import utils.db_api.db_quick_commands as db


@dp.message(
    Command("start"),
    ChatTypeFilter(chat_type=["private"])
)
async def command_start(message: types.Message, state: FSMContext):
    """Регистрация id и username при инициации команды /start"""
    if db.register_user(message):
        await message.answer(f'Добро пожаловать, {message.from_user.username}!')
    await show_menu(message, state)
