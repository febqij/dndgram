from aiogram import Router
from aiogram import types
from aiogram.filters import Command
from aiogram import F
from aiogram import html
from aiogram.fsm.context import FSMContext

import utils.db_api.db_quick_commands as db
from utils.filters.chat_type import ChatTypeFilter
import utils.keyboards as kb
from utils.state import UserState
from utils.db_api.schemas.user import User
from middlewares import ChatHistoryMessageMiddleware

from bot import bot


router_age = Router()
router_age.message(ChatTypeFilter(chat_type=["private"]))
router_age.callback_query.middleware(ChatHistoryMessageMiddleware())


def get_age_text(user: User):
    if user.age:
        return (f"Ваш указанный текущий возраст: {html.code(user.age)}")
    return (
        "Данные о вашем возрасте отсутствуют.\n"
        "Чтобы изменить знчение отправьте в данный диалог сообщение в виде целого числа."
    )


@router_age.callback_query(
    kb.ProfileCallBack.filter(F.button == "age")
)
async def edit_age_callback(callbackquery: types.CallbackQuery, state: FSMContext):
    await state.set_state(UserState.age)

    message: types.Message = callbackquery.message
    user: User = await db.select_user(callbackquery.from_user.id)

    await message.edit_text(
        text=get_age_text(user),
        reply_markup=kb.get_kb_age()
    )


@router_age.message(
    Command("age")
)
async def edit_age_command(
    message: types.Message,
    state: FSMContext
):
    await state.set_state(UserState.age)

    user: User = await db.select_user(message.from_user.id)

    try:
        await message.answer(
                text=get_age_text(user),
                reply_markup=kb.get_kb_age()
            )
    finally:
        await bot.delete_message(
            chat_id=message.from_user.id,
            message_id=message.message_id
        )
