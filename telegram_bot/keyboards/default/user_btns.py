from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from utils.bot_context import languages


remove_btn = ReplyKeyboardRemove()


async def start_command_btn(lang: str):
    btn = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text=languages[lang]["reply_button"]["search_text"]),
            ],
            [
                KeyboardButton(text=languages[lang]["reply_button"]["service_text"]),
                KeyboardButton(text=languages[lang]["reply_button"]["product_text"])
            ],
            [
                KeyboardButton(text=languages[lang]["reply_button"]["admin_text"]),
                KeyboardButton(text=languages[lang]["reply_button"]["profile_text"]),
            ],
            [
                KeyboardButton(text=languages[lang]["reply_button"]["about_text"]),
            ]
        ]
    )
    return btn


async def send_phone_number_btn(lang: str):
    btn = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text=languages[lang]["reply_button"]["phone_number_text"], request_contact=True)
            ]
        ]
    )
    return btn


async def regions_btn(lang: str, regions: list):
    btn = ReplyKeyboardBuilder()
    btn.row(
        KeyboardButton(text=languages[lang]["reply_button"]["only_uzbekistan"]),
        width=1
    )
    btn.add(
        *[KeyboardButton(text=item['name']) for item in regions],
        KeyboardButton(text=languages[lang]["reply_button"]["back_text"])
    )
    btn.adjust(2)
    return btn.as_markup(resize_keyboard=True)


async def subs_btn(cities: list, lang=False):
    btn = ReplyKeyboardBuilder()
    btn.add(
        KeyboardButton(text=cities[0])
    )
    btn.add(
        *[KeyboardButton(text=item) for item in cities[1:]]
    )
    if lang:
        btn.add(
            KeyboardButton(text=languages[lang]["reply_button"]["back_text"])
        )
    btn.adjust(2)
    return btn.as_markup(resize_keyboard=True)


async def profile_btn(lang: str):
    btn = ReplyKeyboardBuilder()
    btn.button(text=languages[lang]['reply_button']['edit_user_info'])
    btn.button(text=languages[lang]['reply_button']['edit_language_text'])
    btn.add(
        KeyboardButton(text=languages[lang]['reply_button']['back_text'])
    )

    btn.adjust(2, repeat=True)
    return btn.as_markup(resize_keyboard=True)


async def choose_category_btn(lang: str, categories: list):
    btn = ReplyKeyboardBuilder()
    btn.add(
        *[KeyboardButton(text=item['name']) for item in categories],

        KeyboardButton(text=languages[lang]['reply_button']['back_text'])
    )
    btn.adjust(2)
    return btn.as_markup(resize_keyboard=True)


async def search_category_btn(lang: str, categories: list):
    btn = ReplyKeyboardBuilder()
    btn.add(
        *[KeyboardButton(text=item) for item in categories],

        KeyboardButton(text=languages[lang]['reply_button']['back_text'])
    )
    btn.adjust(2)
    return btn.as_markup(resize_keyboard=True)

