from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import CancelHandler, SkipHandler
from aiogram.types import Message

from telegram_bot.handlers.users.users import choose_language_handler
from telegram_bot.utils.api_connections import get_user_language, add_user


class SetUserLanguageMiddleware(BaseMiddleware):

    async def on_process_message(self, message: Message, data: dict):
        user_id = message.from_user.id
        user = await add_user(
            user_id=message.from_user.id,
            username=message.from_user.username
        )
        user_language = (await get_user_language(user_id))['language']
        message.from_user.language_code = user_language
        #
        # if not user['is_active']:
        #     await choose_language_handler(message)

