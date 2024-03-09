from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils.bot_context import languages

from data.config import API_URL


class Lang(CallbackData, prefix='lang'):
    lang: str


class Pagination(CallbackData, prefix='prev'):
    page: int


class Staff(CallbackData, prefix='stuff'):
    id: int


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


async def service_pagination_btn(staffs: list, current_page: int, total: int, in_page: int = 3):
    btn = InlineKeyboardBuilder()
    pages = round(total/in_page)
    prev_p = current_page - 1 if current_page > 1 else 1
    next_p = current_page + 1 if current_page < total else pages
    btn.add(
        *[InlineKeyboardButton(text=f"{n}", callback_data=Staff(id=item['id']).pack()) for n, item in enumerate(staffs, 1)]
    )
    if total > in_page:
        btn.row(
            InlineKeyboardButton(text="◀️", callback_data=Pagination(page=prev_p).pack()),
            InlineKeyboardButton(text=f"{current_page}/{pages}", callback_data=f"pages"),
            InlineKeyboardButton(text="▶️️", callback_data=Pagination(page=next_p).pack()),
            width=3
        )
    return btn.as_markup()


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
