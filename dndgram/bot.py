import asyncio
from aiogram import Bot, Dispatcher, types, filters

from data.config import config


bot = Bot(token=config.BOT_TOKEN.get_secret_value(), parse_mode="HTML")

dp = Dispatcher()


async def main():
    from handlers import dp
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
