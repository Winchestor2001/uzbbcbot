from typing import Union, Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.dispatcher.event.bases import CancelHandler
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from telegram_bot.handlers.users.users import choose_language_handler
from telegram_bot.states.AllStates import UserStates
from telegram_bot.utils.api_connections import get_user_language, add_user
from telegram_bot.utils.bot_context import languages


class SetUserLanguageMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any],
    ) -> Any:
        user_id = event.from_user.id
        state: FSMContext = data.get('state')
        current_state = await state.get_state()
        await add_user(
            user_id=event.from_user.id,
            username=event.from_user.username
        )
        user = (await get_user_language(user_id))
        custom_data = {
            "lang": user['language'],
            "is_active": user['is_active'],
        }
        data.update(custom_data)
        if not user['is_active'] and current_state is None:
            return await choose_language_handler(event, state, custom_data)

        return await handler(event, data)
