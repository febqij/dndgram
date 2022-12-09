from aiogram import Router
from aiogram import types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

import utils.db_api.db_quick_commands as db
from utils.keyboards import get_kb_menu
from utils.state import UserState
from bot import bot


router_menu = Router()


@router_menu.message(Command("menu"))
async def show_menu(message: types.Message, state: FSMContext):
    await state.set_state(UserState.menu)

    await db.register_user(message)

    try:
        await message.answer(
            "Меню навигации:",
            reply_markup=get_kb_menu()
        )
    finally:
        await bot.delete_message(
            chat_id=message.from_user.id,
            message_id=message.message_id
        )
