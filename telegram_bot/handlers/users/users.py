from aiogram import F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.enums.content_type import ContentType

from keyboards.default.user_btns import start_command_btn
from keyboards.inline.user_btns import choose_language_btn
from loader import dp
from utils.bot_context import languages

from states.AllStates import UserStates
from utils.api_connections import update_user_language
from aiogram import Router

from keyboards.default.user_btns import send_phone_number_btn, regions_btn
from keyboards.inline.user_btns import Lang
from utils.api_connections import send_verify_code, get_regions, verify_user
from utils.usefull_functions import _short

from utils.api_connections import get_user_info

user_route = Router()


@user_route.message(CommandStart())
async def start_command(message: Message):
    lang = message.from_user.language_code
    context = languages[lang]['start_command']
    btn = await start_command_btn(lang)
    await message.answer(context, reply_markup=btn)


async def choose_language_handler(message: Message, state: FSMContext, data: dict):
    btn = await choose_language_btn()
    await state.update_data(data=data)
    await message.answer("Tilni tanlang\n\nВыберите язык\n\nChoose language", reply_markup=btn)


@user_route.callback_query(Lang.filter())
async def selected_language_callback(c: CallbackQuery, state: FSMContext):
    lang = c.data.split(':')[1]
    data = (await state.get_data())
    await update_user_language(
        user_id=c.from_user.id,
        language=lang
    )
    await c.message.delete()
    if data['is_active']:
        context = languages[lang]['start_command']
        btn = await start_command_btn(lang)
        await c.message.answer(context, reply_markup=btn)
    else:
        btn = await send_phone_number_btn(lang)
        await c.message.answer(languages[lang]['get_phone_number_handler'], reply_markup=btn)
        await state.set_state(UserStates.phone_number)


@user_route.message(UserStates.phone_number, F.content_type.in_({'text', 'contact'}))
async def user_phone_number_state(message: Message, state: FSMContext):
    lang = (await state.get_data())['lang']
    if message.contact:
        phone_number = message.contact.phone_number
    else:
        phone_number = message.text

    code = await send_verify_code(
        user_id=message.from_user.id,
        phone_number=phone_number
    )
    await state.update_data(code=code['code'], phone_number=phone_number)
    await message.answer(languages[lang]['verify_code_text'])
    await state.set_state(UserStates.verify_code)


@user_route.message(UserStates.verify_code, F.text)
async def user_verify_code_state(message: Message, state: FSMContext):
    code = message.text
    data = await state.get_data()
    lang = data['lang']
    if int(code) == data['code']:
        regions = await get_regions()
        btn = await regions_btn(regions)
        await message.answer(languages[lang]['choose_region_handler'], reply_markup=btn)
        await state.set_state(UserStates.region)
    else:
        await message.answer(languages[lang]['wrong_code_text'])


@user_route.message(UserStates.region, F.text)
async def user_region_state(message: Message, state: FSMContext):
    user_region = message.text
    data = await state.get_data()
    await verify_user(
        user_id=message.from_user.id,
        phone_number=data['phone_number'],
        region=user_region
    )
    await state.set_state(None)
    await start_command(message)


@user_route.message(F.text, F.in_(_short('profile_text')))
async def user_profile_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    info = await get_user_info(user_id)
    print(info)




