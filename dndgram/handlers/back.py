from aiogram import Router
from aiogram import types
from aiogram.filters import Command
from aiogram import F
from aiogram.fsm.context import FSMContext

import utils.keyboards as kb
import utils.db_api.db_quick_commands as db
from utils.db_api.schemas.user import User
from utils.filters.chat_type import ChatTypeFilter
from utils.state import UserState
from utils.state import UserState
from bot import bot


router_back = Router()


@router_back.callback_query(kb.ProfileCallBack.filter(F.button == "back"))
async def back_to_menu(callbackquery: types.CallbackQuery, state: FSMContext):

    message: types.Message = callbackquery.message

    from handlers.menu import get_menu_text

    await message.edit_text(
        text=get_menu_text(),
        reply_markup=kb.get_kb_menu()
    )


@router_back.message(
    Command("back"),
    ChatTypeFilter(chat_type=["private"]),
    UserState.profile
)
async def show_profile_command(
    message: types.Message,
    state: FSMContext
):
    from handlers.menu import show_menu
    await show_menu(message, state)
