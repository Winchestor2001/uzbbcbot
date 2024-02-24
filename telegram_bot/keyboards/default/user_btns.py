from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from utils.bot_context import languages


async def start_command_btn(lang: str):
    btn = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn.add(
        KeyboardButton(languages[lang]["reply_button"]["service_text"]),
        KeyboardButton(languages[lang]["reply_button"]["product_text"]),
        KeyboardButton(languages[lang]["reply_button"]["about_text"]),
        KeyboardButton(languages[lang]["reply_button"]["admin_text"]),
    )
    return btn


