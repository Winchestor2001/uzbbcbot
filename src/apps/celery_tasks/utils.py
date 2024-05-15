import requests
from environs import Env
import json
from telegram_bot.utils.bot_context import languages
from datetime import datetime

env = Env()
env.read_env()


def send_message_to_user(user, lang: str, receiver, datatype):
    url = f"https://api.telegram.org/bot{env.str('BOT_TOKEN')}/sendMessage"
    inline_keyboard = [
        [{"text": languages[lang]['reply_button']['called_text'], "callback_data": f"called:{datatype}:{receiver.id}"}],
        [{"text": languages[lang]['reply_button']['no_called_text'], "callback_data": f"no_called"}]
    ]
    reply_markup = {"inline_keyboard": inline_keyboard}
    date = user.created_at.strftime("%H:%M")
    params = {
        "chat_id": user.user.user_id,
        "text": languages[lang]['called_text'].format(date, receiver.fullname),
        "reply_markup": json.dumps(reply_markup),
        "parse_mode": "HTML"
    }
    response = requests.post(url, data=params)
    if response.status_code == 200:
        user.delete()
