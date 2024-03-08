import asyncio
import logging
import sys

from loader import dp, bot
import middlewares, filters, handlers
from utils.set_bot_commands import set_default_commands


async def on_startup():
    await set_default_commands(bot)

    dp.include_routers(*handlers.routers_list)

    await bot.delete_webhook(drop_pending_updates=True)  # skip_updates
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(on_startup())

