from aiogram.types import Message
from aiogram.filters import Filter
from utils.bot_context import languages


class BtnLangCheck(Filter):

    def __init__(self, text: str) -> None:
        self.key = text

    async def __call__(self, message: Message) -> bool:
        text = message.text
        result = []

        for item in languages:
            result.append(
                languages[item]['reply_button'][self.key]
            )
        return text in result




