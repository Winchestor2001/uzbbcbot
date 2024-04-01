import logging
from typing import Union, Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.dispatcher.event.bases import CancelHandler
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, TelegramObject

from handlers.users.users import choose_language_handler
from states.AllStates import UserStates
from utils.api_connections import get_user_language, add_user
from utils.bot_context import languages


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
        current_data = await state.get_data()
        await add_user(
            user_id=event.from_user.id,
            username=event.from_user.username
        )
        user = (await get_user_language(user_id))
        custom_data = {
            "lang": user['language'],
            "is_active": user['is_active'],
        }
        custom_data.update(current_data)
        data['user_data'] = custom_data
        await state.set_data(custom_data)
        if not user['is_active'] and current_state is None and not getattr(event, 'data', False):
            return await choose_language_handler(event)

        return await handler(event, data)
