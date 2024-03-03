from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from utils.bot_context import languages


async def start_command_btn(lang: str):
    btn = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
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


async def regions_btn(regions: list):
    btn = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text=item['name'])
            ]
            for item in regions
        ]
    )
    return btn


async def profile_btn(lang: str):
    btn = ReplyKeyboardBuilder()
    btn.button(text=languages[lang]['reply_button']['edit_phone_number_text'])
    btn.button(text=languages[lang]['reply_button']['edit_region_text'])
    btn.button(text=languages[lang]['reply_button']['edit_language_text'])
    btn.button(text=languages[lang]['reply_button']['edit_language_text'])
    btn.add(
        KeyboardButton(text=languages[lang]['reply_button']['back_text'])
    )

    btn.adjust(2, repeat=True)
    return btn.as_markup(resize_keyboard=True)


async def location_btn(lang: str):
    btn = ReplyKeyboardBuilder()
    btn.add(
        KeyboardButton(text=languages[lang]['reply_button']['location_text'], request_location=True)
    )
    return btn.as_markup(resize_keyboard=True)



