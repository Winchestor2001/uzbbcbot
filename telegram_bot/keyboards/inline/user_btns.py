from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils.bot_context import languages

from data.config import API_URL


class Lang(CallbackData, prefix='lang'):
    lang: str


class Pagination(CallbackData, prefix=''):
    page: int


class Staff(CallbackData, prefix='stuff'):
    id: int


class Product(CallbackData, prefix='product'):
    id: int


class StaffComment(CallbackData, prefix='comment'):
    id: int


class ProductComment(CallbackData, prefix='product_comment'):
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


async def service_btn(lang: str, phone_number, stuff_id: int):
    btn = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=languages[lang]['reply_button']['call_text'].format(phone_number),
                    url=f"{API_URL}/call/?phone={phone_number}"),
            ],
            [
                InlineKeyboardButton(text=languages[lang]['reply_button']['comment_text'],
                                     callback_data=StaffComment(id=stuff_id).pack())
            ]
        ]
    )
    return btn


async def service_pagination_btn(staffs: list, current_page: int, total: int, in_page: int = 3):
    btn = InlineKeyboardBuilder()
    pages = round(total / in_page)
    prev_p = current_page - 1 if current_page > 1 else 1
    next_p = current_page + 1 if current_page < pages else pages
    btn.add(
        *[InlineKeyboardButton(text=f"{n}", callback_data=Staff(id=item['id']).pack()) for n, item in
          enumerate(staffs, 1)]
    )
    if total > in_page:
        btn.row(
            InlineKeyboardButton(text="◀️", callback_data=Pagination(prefix='prev', page=prev_p).pack()),
            InlineKeyboardButton(text=f"{current_page}/{pages}", callback_data=f"pages"),
            InlineKeyboardButton(text="▶️️", callback_data=Pagination(prefix='next', page=next_p).pack()),
            width=3
        )
    return btn.as_markup()


async def product_pagination_btn(staffs: list, current_page: int, total: int, in_page: int = 3):
    btn = InlineKeyboardBuilder()
    pages = round(total / in_page)
    prev_p = current_page - 1 if current_page > 1 else 1
    next_p = current_page + 1 if current_page < pages else pages
    btn.add(
        *[InlineKeyboardButton(text=f"{n}", callback_data=Product(id=item['id']).pack()) for n, item in
          enumerate(staffs, 1)]
    )
    if total > in_page:
        btn.row(
            InlineKeyboardButton(text="◀️", callback_data=Pagination(prefix='product_prev', page=prev_p).pack()),
            InlineKeyboardButton(text=f"{current_page}/{pages}", callback_data=f"pages"),
            InlineKeyboardButton(text="▶️️", callback_data=Pagination(prefix='product_next', page=next_p).pack()),
            width=3
        )
    return btn.as_markup()


async def stuff_comment_btn(comments: int):
    btn = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Back", callback_data="back")
            ]
        ]
    )
    if comments > 1:
        btn.inline_keyboard.append([
                InlineKeyboardButton(text="◀️", callback_data="prev"),
                InlineKeyboardButton(text="▶️", callback_data="next"),
            ])
    return btn


async def product_btn(lang: str, phone_number, product_id: int):
    btn = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=languages[lang]['reply_button']['call_text'].format(phone_number),
                    url=f"{API_URL}/call/?phone={phone_number}"),
            ],
            [
                InlineKeyboardButton(text=languages[lang]['reply_button']['comment_text'],
                                     callback_data=ProductComment(id=product_id).pack())
            ]
        ]
    )
    return btn


async def product_comment_btn(comments: int):
    btn = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Back", callback_data="back")
            ]
        ]
    )
    if comments > 1:
        btn.inline_keyboard.append([
                InlineKeyboardButton(text="◀️", callback_data="prev"),
                InlineKeyboardButton(text="▶️", callback_data="next"),
            ])
    return btn

