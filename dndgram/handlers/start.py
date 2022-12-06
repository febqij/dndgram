from aiogram import types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot import dp
from handlers.menu import show_menu
from utils.filters.chat_type import ChatTypeFilter


@dp.message(
    Command("start"),
    ChatTypeFilter(chat_type=["private"])
)
async def command_start(message: types.Message, state: FSMContext):
    """Регистрация id и username при инициации команды /start"""
    await show_menu(message, state)
