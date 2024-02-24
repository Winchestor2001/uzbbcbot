from aiogram import Dispatcher

from loader import dp

from .check_user_language import SetUserLanguageMiddleware
from .throttling import ThrottlingMiddleware


if __name__ == "middlewares":
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(SetUserLanguageMiddleware())
