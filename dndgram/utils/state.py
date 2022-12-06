from aiogram.fsm.state import StatesGroup, State


class UserState(StatesGroup):
    menu = State()
    profile = State()
    editing = State()
    editing_field = State()
    age = State()
    gender = State()
    preferences = State()
    bio = State()
