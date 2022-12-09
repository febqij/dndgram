from aiogram import Router
from aiogram import types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from utils.db_api.schemas.user import User
import utils.db_api.db_quick_commands as db
import utils.keyboards as kb
from utils.keyboards import get_kb_menu
from utils.state import UserState

from bot import bot


router_menu = Router()


def get_menu_text():
    return "Меню навигации:"


@router_menu.message(Command("menu"))
async def show_menu(message: types.Message, state: FSMContext):
    await state.set_state(UserState.menu)

    await db.register_user(message)

    try:
        await message.answer(
            get_menu_text(),
            reply_markup=get_kb_menu()
        )
    finally:
        await bot.delete_message(
            chat_id=message.from_user.id,
            message_id=message.message_id
        )



async def back_to_menu(callbackquery: types.CallbackQuery, state: FSMContext):
    await state.set_state(UserState.menu)

    message: types.Message = callbackquery.message

    await message.edit_text(
        text=get_menu_text(),
        reply_markup=kb.get_kb_menu()
    )