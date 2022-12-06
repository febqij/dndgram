from aiogram import Router
from aiogram import types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from utils.keyboards.kb_menu import get_kb_menu
from utils.state import UserState


router = Router()

@router.message(Command("menu"))
async def show_menu(message: types.Message, state: FSMContext):
    await state.set_state(UserState.menu)

    # TODO: Регистрация пользователя в БД

    # TODO: Вывод nline-клавиатуры
    await message.answer(
        "Меню навигации:",
        reply_markup=get_kb_menu()
    )
