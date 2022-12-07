import asyncio
from aiogram import Bot, Dispatcher, types, filters

from data.config import config
from utils.on_startup import on_startup_notify
from utils.set_bot_commands import set_default_commands


bot = Bot(token=config.BOT_TOKEN.get_secret_value(), parse_mode="HTML")

dp = Dispatcher()


async def main():
    from handlers import dp, router

    on_startup_notify()

    await bot.delete_webhook(drop_pending_updates=True)
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
