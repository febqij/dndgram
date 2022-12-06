from aiogram import types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot import dp
from handlers.menu import show_menu


@dp.message(Command("start"))
async def command_start(message: types.Message, state: FSMContext):
    """Регистрация id и username при инициации команды /start"""
    await show_menu(message, state)
