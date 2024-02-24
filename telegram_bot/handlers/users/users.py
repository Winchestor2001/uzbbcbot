from aiogram import Dispatcher
from aiogram.types import *

from filters import IsActiveFilter
from keyboards.default.user_btns import start_command_btn
from keyboards.inline.user_btns import choose_language_btn
from loader import dp
from utils.bot_context import languages

from telegram_bot.utils.api_connections import update_user_language


async def start_command(message: Message):
    lang = message.from_user.language_code
    context = languages[lang]['start_command']
    btn = await start_command_btn(lang)
    await message.answer(context, reply_markup=btn)


async def choose_language_handler(message: Message):
    lang = message.from_user.language_code
    btn = await choose_language_btn(lang)
    await message.answer("Tilni tanlang\n\nВыберите язык\n\nChoose language", reply_markup=btn)


async def selected_language_callback(c: CallbackQuery):
    lang = c.data.split(':')[1]
    await update_user_language(
        user_id=c.from_user.id,
        language=lang
    )
    await c.message.delete()
    context = languages[lang]['start_command']
    btn = await start_command_btn(lang)
    await c.message.answer(context, reply_markup=btn)


def register_users_py(dp: Dispatcher):
    dp.register_message_handler(start_command, IsActiveFilter(), commands=['start'])
    dp.register_message_handler(choose_language_handler, commands=['lang'])

    dp.register_callback_query_handler(selected_language_callback, text_contains='lang')


