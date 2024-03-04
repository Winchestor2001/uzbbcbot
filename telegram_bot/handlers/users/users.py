from aiogram import F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.formatting import PhoneNumber

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

from utils.api_connections import get_user_info

from filters.user_filters import BtnLangCheck
from keyboards.default.user_btns import profile_btn

from keyboards.default.user_btns import location_btn
from keyboards.inline.user_btns import service_btn
from utils.api_connections import search_service_by_location
from utils.usefull_functions import location_info

from bot_api.utils import calc_distance

user_route = Router()


@user_route.message(CommandStart())
async def start_command(message: Message, state: FSMContext):
    lang = (await state.get_data())['lang']
    context = languages[lang]['start_command']
    btn = await start_command_btn(lang)
    await message.answer(context, reply_markup=btn)


async def choose_language_handler(message: Message, state: FSMContext):
    btn = await choose_language_btn()
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
    await start_command(message, state)


@user_route.message(BtnLangCheck('profile_text'))
async def user_profile_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    lang = data['lang']
    info = await get_user_info(user_id)

    context = languages[lang]['profile_text'].format(
        info['user_id'], info['username'], info['region'], info['phone_number']
    )
    btn = await profile_btn(lang)
    await message.answer(context, reply_markup=btn)


@user_route.message(BtnLangCheck('back_text'))
async def user_back_handler(message: Message, state: FSMContext):
    await start_command(message, state)


@user_route.message(BtnLangCheck('service_text'))
async def service_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data['lang']
    context = languages[lang]['location_text']
    btn = await location_btn(lang)
    await message.answer(context, reply_markup=btn)
    await state.set_state(UserStates.location)


@user_route.message(BtnLangCheck('product_text'))
async def product_handler(message: Message, state: FSMContext):
    pass


@user_route.message(BtnLangCheck('about_text'))
async def about_handler(message: Message, state: FSMContext):
    pass


@user_route.message(BtnLangCheck('admin_text'))
async def admin_handler(message: Message, state: FSMContext):
    pass


@user_route.message(UserStates.location)
async def location_state(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data['lang']
    lat = message.location.latitude
    lon = message.location.longitude
    btn = await start_command_btn(lang)
    services = await search_service_by_location(message.from_user.id, lat, lon)
    loading = await message.answer("⏳", reply_markup=btn)
    await loading.delete()
    for item in services:
        location = calc_distance(lat, lon, item['latitude'], item['longitude'])
        context = languages[lang]['service_info_text'].format(
            item['fullname'], item['professional'], item['price'], item['region'], location
        )
        btn = await service_btn(lang, item['phone_number'])
        await message.answer(context, reply_markup=btn)

    await state.set_state(None)


@user_route.message(BtnLangCheck('edit_user_info'))
async def edit_user_info_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data['lang']
    btn = await send_phone_number_btn(lang)
    await message.answer(languages[lang]['get_phone_number_handler'], reply_markup=btn)
    await state.set_state(UserStates.phone_number)


@user_route.message(BtnLangCheck('edit_language_text'))
async def edit_language_handler(message: Message, state: FSMContext):
    await choose_language_handler(message, state)



