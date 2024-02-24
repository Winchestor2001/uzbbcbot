from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.bot_context import languages


async def choose_language_btn(lang: str):
    btn = InlineKeyboardMarkup(row_width=2)
    btn.add(
        InlineKeyboardButton(text="🇺🇿 UZ", callback_data="lang:uz"),
        InlineKeyboardButton(text="🇷🇺 RU", callback_data="lang:ru"),
        InlineKeyboardButton(text="🇺🇸 EN", callback_data="lang:en"),
    )
    return btn



