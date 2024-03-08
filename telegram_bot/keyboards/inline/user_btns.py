from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.bot_context import languages

from data.config import API_URL


class Lang(CallbackData, prefix='lang'):
    lang: str


async def choose_language_btn():
    btn = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🇺🇿 UZ",
                    callback_data=Lang(lang='uz').pack(),
                ),
                InlineKeyboardButton(
                    text="🇷🇺 RU",
                    callback_data=Lang(lang='ru').pack(),
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🇺🇸 EN",
                    callback_data=Lang(lang='en').pack(),
                )
            ]
        ]
    )
    return btn


async def service_btn(lang: str, phone_number):
    btn = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=languages[lang]['reply_button']['call_text'].format(phone_number),
                    url=f"{API_URL}/call/?phone={phone_number}"),
            ],
            [
                InlineKeyboardButton(text="Comment", callback_data="comment")
            ]
        ]
    )
    return btn


async def test_comment_btn():
    btn = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="<--", callback_data="prev"),
                InlineKeyboardButton(text="1/2", callback_data="0"),
                InlineKeyboardButton(text="-->", callback_data="next"),
            ],
            [
                InlineKeyboardButton(text="Back", callback_data="back")
            ]
        ]
    )
    return btn
