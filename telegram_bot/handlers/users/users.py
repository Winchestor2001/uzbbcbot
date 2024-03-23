from aiogram import F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from keyboards.default.user_btns import search_category_btn, start_command_btn
from keyboards.inline.user_btns import choose_language_btn
from utils.bot_context import languages

from states.AllStates import UserStates
from utils.api_connections import search_by_text, update_user_language
from aiogram import Router

from keyboards.default.user_btns import send_phone_number_btn, regions_btn
from keyboards.inline.user_btns import Lang
from utils.api_connections import get_regions, verify_user

from utils.api_connections import get_user_info

from filters.user_filters import BtnLangCheck, SearchTextLength
from keyboards.default.user_btns import profile_btn

from keyboards.default.user_btns import subs_btn
from utils.usefull_functions import get_region_cities

router = Router()


@router.message(CommandStart())
async def start_command(message: Message, state: FSMContext):
    lang = (await state.get_data())['lang']
    context = languages[lang]['start_command']
    btn = await start_command_btn(lang)
    await message.answer(context, reply_markup=btn)
    await state.clear()


async def choose_language_handler(message: Message):
    btn = await choose_language_btn()
    await message.answer("Tilni tanlang\n\nВыберите язык\n\nChoose language", reply_markup=btn)


@router.callback_query(Lang.filter())
async def selected_language_callback(c: CallbackQuery, state: FSMContext):
    lang = c.data.split(':')[1]
    data = (await state.get_data())
    await update_user_language(
        user_id=c.from_user.id,
        language=lang
    )
    await state.update_data(lang=lang)
    await c.message.delete()
    if data['is_active']:
        context = languages[lang]['start_command']
        btn = await start_command_btn(lang)
        await c.message.answer(context, reply_markup=btn)
        await state.set_state(None)
    else:
        btn = await send_phone_number_btn(lang)
        await c.message.answer(languages[lang]['get_phone_number_handler'], reply_markup=btn)
        await state.set_state(UserStates.phone_number)


@router.message(UserStates.phone_number, F.content_type.in_({'text', 'contact'}))
async def user_phone_number_state(message: Message, state: FSMContext):
    lang = (await state.get_data())['lang']
    if message.contact:
        phone_number = message.contact.phone_number
    else:
        phone_number = message.text

    await state.update_data(phone_number=phone_number)
    regions = await get_regions()
    btn = await regions_btn(lang, regions)
    await message.answer(languages[lang]['choose_region_handler'], reply_markup=btn)
    await state.set_state(UserStates.region)


@router.message(UserStates.region, F.text)
async def user_region_state(message: Message, state: FSMContext):
    user_region = message.text
    data = await state.get_data()
    if languages[data['lang']]['reply_button']['only_uzbekistan'] == user_region:
        await verify_user(
            user_id=message.from_user.id,
            phone_number=data['phone_number'],
            city='no',
        )
        await state.set_state(None)
        await start_command(message, state)
    else:
        await state.update_data(region=user_region)
        cities = await get_region_cities((await get_regions()), user_region)
        user_region = languages[data['lang']]['reply_button']['only_cities'].format(user_region)
        cities.insert(0, user_region)
        btn = await subs_btn(cities)
        await message.answer(languages[data['lang']]['choose_city_handler'], reply_markup=btn)
        await state.set_state(UserStates.city)


@router.message(UserStates.city, F.text)
async def user_city_state(message: Message, state: FSMContext):
    user_city = message.text
    data = await state.get_data()
    if data['region'] in user_city:
        user_city = data['region']
    await verify_user(
        user_id=message.from_user.id,
        phone_number=data['phone_number'],
        city=user_city,
    )
    await state.set_state(None)
    await start_command(message, state)


@router.message(BtnLangCheck('profile_text'))
async def user_profile_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    lang = data['lang']
    info = await get_user_info(user_id)
    city = languages[lang]['reply_button']['only_uzbekistan'] if info['all_regions'] else info['city']
    context = languages[lang]['profile_text'].format(
        info['user_id'], info['username'], city, info['phone_number']
    )
    btn = await profile_btn(lang)
    await message.answer(context, reply_markup=btn)


@router.message(BtnLangCheck('back_text'))
async def user_back_handler(message: Message, state: FSMContext):
    await start_command(message, state)


@router.message(BtnLangCheck('about_text'))
async def about_handler(message: Message, state: FSMContext):
    pass


@router.message(BtnLangCheck('admin_text'))
async def admin_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data['lang']
    context = languages[lang]['admin_text']
    await message.answer(context)


@router.message(BtnLangCheck('edit_user_info'))
async def edit_user_info_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data['lang']
    btn = await send_phone_number_btn(lang)
    await message.answer(languages[lang]['get_phone_number_handler'], reply_markup=btn)
    await state.set_state(UserStates.phone_number)


@router.message(BtnLangCheck('edit_language_text'))
async def edit_language_handler(message: Message):
    await choose_language_handler(message)


@router.callback_query(F.data == 'back')
async def back_callback(c: CallbackQuery, state: FSMContext):
    await c.answer()
    data = await state.get_data()
    await c.message.edit_text(data['text'], reply_markup=data['btn'])


@router.callback_query(F.data == 'next')
async def next_callback(c: CallbackQuery, state: FSMContext):
    await c.answer()
    data = await state.get_data()
    lang = data['lang']
    in_comment = data['in_comment']
    in_comment += 1
    if in_comment < len(data['comments']):
        await state.update_data(in_comment=in_comment)
        context = languages[lang]['comment_text'].format(data['comments'][in_comment]['tg_user'], data['comments'][in_comment]['comment'])
        await c.message.edit_text(context, reply_markup=c.message.reply_markup)


@router.callback_query(F.data == 'prev')
async def prev_callback(c: CallbackQuery, state: FSMContext):
    await c.answer()
    data = await state.get_data()
    lang = data['lang']
    in_comment = data['in_comment']
    if in_comment >= 0:
        in_comment -= 1
        await state.update_data(in_comment=in_comment)
        context = languages[lang]['comment_text'].format(data['comments'][in_comment]['tg_user'], data['comments'][in_comment]['comment'])
        await c.message.edit_text(context, reply_markup=c.message.reply_markup)


@router.callback_query(F.data.startswith('called'))
async def user_called_callback(c: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data['lang']
    _, datatype, receiver = c.data.split(':')
    await state.update_data(datatype=datatype, receiver=receiver)
    await c.message.edit_text(languages[lang]['write_comment_text'])
    await state.set_state(UserStates.add_comment)


@router.message(UserStates.add_comment)
async def user_add_comment_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data['lang']
    await state.update_data(comment=message.text)
    await message.answer(languages[lang]['write_rating_text'])
    await state.set_state(UserStates.add_rating)


@router.message(UserStates.add_rating, F.text.isdigit())
async def user_add_rating_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data['lang']
    rating = int(message.text)
    if 0 < rating > 11:
        await message.answer(languages[lang]['added_comment'])
        await state.set_state(None)


@router.callback_query(F.data == 'no_called')
async def user_no_called_callback(c: CallbackQuery):
    await c.message.delete()


@router.message(BtnLangCheck('search_text'))
async def user_search_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data['lang']
    context = languages[lang]['search_text']
    await message.answer(context)
    await state.set_state(UserStates.search)


@router.message(UserStates.search, F.text, SearchTextLength())
async def user_search_state(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data['lang']
    search_text = message.text
    find_data = await search_by_text(
        user_id=message.from_user.id,
        text=search_text
    )
    if find_data:
        context = "🔎"
        btn = await search_category_btn(lang, find_data['result'])
        await message.answer(context, reply_markup=btn)
        await state.set_state(eval(f"UserStates.{find_data['to_state']}"))
    else:
        context = languages[lang]['no_find_text']
        await message.answer(context)
