from aiogram import types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot import dp
from utils.state import UserState


@dp.message(Command("menu"))
async def show_menu(message: types.Message, state: FSMContext):
    await state.set_state(UserState.menu)

    # TODO: Регистрация пользователя в БД

    # TODO: Вывод nline-клавиатуры

    await message.answer("Меню навигации:")
