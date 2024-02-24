from aiogram import executor

from loader import dp
import middlewares, filters, handlers
from telegram_bot.handlers.users.users import register_users_py
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    await set_default_commands(dispatcher)

    register_users_py(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)

