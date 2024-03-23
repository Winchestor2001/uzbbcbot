from aiogram.types import Message, CallbackQuery
from aiogram.filters import Filter
from utils.bot_context import languages
from aiogram.fsm.context import FSMContext


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


class SearchTextLength(Filter):
    async def __call__(self, message: Message, state: FSMContext) -> bool:
        text = message.text
        if len(text) >= 3:
            result = True
        else:
            result = False
            lang = (await state.get_data())['lang']
            context = languages[lang]['min_text']
            await message.answer(context)
        return result

