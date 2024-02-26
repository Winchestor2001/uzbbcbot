import asyncio
import logging
import sys

from loader import dp, bot
import middlewares, filters, handlers
# from handlers.users.users import register_users_py
from utils.set_bot_commands import set_default_commands


async def on_startup():
    await set_default_commands(bot)

    dp.include_routers(*handlers.routers_list)
    # register_users_py(dp)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(on_startup())
