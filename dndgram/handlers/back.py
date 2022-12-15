from aiogram import Router
from aiogram import types
from aiogram.filters import Command
from aiogram import F
from aiogram.fsm.context import FSMContext

import utils.keyboards as kb
from utils.db_api.schemas.user import User
import utils.db_api.db_quick_commands as dbqc
from utils.filters.chat_type import ChatTypeFilter
from utils.state import UserState

from handlers.profile import show_profile_callback, show_profile_command

import middlewares as mdlw

from bot import bot


router_back = Router()
router_back.message(ChatTypeFilter(chat_type=["private"]))
router_back.callback_query.middleware(mdlw.ChatHistoryCallbackQueryMiddleware())
router_back.message.middleware(mdlw.ChatHistoryMessageMiddleware())


@router_back.callback_query(kb.ProfileCallBack.filter(F.button == "back"))
async def back_to_menu(callbackquery: types.CallbackQuery, state: FSMContext):

    message: types.Message = callbackquery.message

    from handlers.menu import get_menu_text

    await message.edit_text(
        text=get_menu_text(),
        reply_markup=kb.get_kb_menu()
    )


@router_back.message(Command("back"), UserState.profile)
async def back_to_menu_command(message: types.Message, state: FSMContext):
    from handlers.menu import show_menu
    await show_menu(message, state)


@router_back.callback_query(kb.AgeCallBack.filter(F.button == "back"))
@router_back.callback_query(kb.GenderCallBack.filter(F.button == "back"))
@router_back.callback_query(kb.PreferencesCallBack.filter(F.button == "back"))
@router_back.callback_query(kb.BioCallBack.filter(F.button == "back"))
@router_back.callback_query(kb.LocationCallBack.filter(F.button == "back"))
async def back_to_profile_from_age(callbackquery: types.CallbackQuery, state: FSMContext):
    await show_profile_callback(callbackquery, state)


@router_back.message(Command("back"), UserState.age)
@router_back.message(Command("back"), UserState.gender)
@router_back.message(Command("back"), UserState.preferences)
@router_back.message(Command("back"), UserState.bio)
@router_back.message(Command("back"), UserState.location)
async def back_to_profile_command_from_age(message: types.Message, state: FSMContext):
    user = await dbqc.get_user_mesages(message.from_user.id)
    await show_profile_command(message, state)
    await mdlw.message_cleaner(user[0])
