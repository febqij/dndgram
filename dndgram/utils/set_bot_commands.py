from aiogram import types
from aiogram.methods.set_my_commands import SetMyCommands

from bot import dp


@dp.startup()
async def set_default_commands():
    SetMyCommands(
        commands=[
            types.BotCommand(command='start', description='Запустить бота'),
            types.BotCommand(command='menu', description='Главное меню'),
        ]
    )
