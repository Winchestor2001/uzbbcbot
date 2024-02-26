from aiogram import Dispatcher

from loader import dp

from .check_user_language import SetUserLanguageMiddleware


if __name__ == "middlewares":
    # dp.middleware.setup(ThrottlingMiddleware())
    dp.message.outer_middleware(SetUserLanguageMiddleware())
    pass

