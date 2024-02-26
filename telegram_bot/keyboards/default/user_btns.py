from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
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
                KeyboardButton(text=languages[lang]["reply_button"]["about_text"]),
                KeyboardButton(text=languages[lang]["reply_button"]["admin_text"]),
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


