import asyncio
from aiogram import Bot, Dispatcher, types, filters

from data.config import config


bot = Bot(token=config.BOT_TOKEN.get_secret_value(), parse_mode="HTML")

dp = Dispatcher()


async def main():
    import handlers

    from utils.on_startup import on_startup_chemas_create
    from utils.set_bot_commands import set_default_commands

    await on_startup_chemas_create()
    await set_default_commands()

    await bot.delete_webhook(drop_pending_updates=True)

    handlers.dp.include_router(handlers.router_menu)
    handlers.dp.include_router(handlers.router_profile)

    await handlers.dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
