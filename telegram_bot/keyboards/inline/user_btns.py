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
                    text=languages[lang]['call_text'],
                    url=f"{API_URL}/call/?phone={phone_number}"),
            ],
        ]
    )
    return btn

