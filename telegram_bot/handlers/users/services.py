import logging
from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from filters.user_filters import BtnLangCheck
from keyboards.default.user_btns import regions_btn, subs_btn, start_command_btn
from keyboards.inline.user_btns import service_pagination_btn, Pagination, Staff, call_btn, \
    StaffComment, stuff_comment_btn
from states.AllStates import UserStates
from utils.api_connections import get_regions, search_services, stuff_service, stuff_comments
from utils.bot_context import languages
from utils.usefull_functions import pagination_context_maker, get_sub_categories

router = Router()


@router.message(BtnLangCheck('service_text'))
async def service_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data['lang']

    regions = await get_regions(lang)
    btn = await regions_btn(lang, regions)
    await message.answer(languages[lang]['choose_region_handler'], reply_markup=btn)
    await state.update_data(action='service')
    await state.set_state(UserStates.region)

    # service_categories = await get_service_categories()
    # await state.update_data(service_categories=service_categories)
    # context = languages[lang]['choose_service_category']
    # btn = await choose_category_btn(lang, service_categories)
    # await message.answer(context, reply_markup=btn)
    # await state.set_state(UserStates.service_category)


@router.message(UserStates.service_category, F.text)
async def service_category_state(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data['lang']
    services = await get_sub_categories(
        obj=data['service_categories'],
        category=message.text,
        key='services',
    )
    context = languages[lang]['choose_service_category']
    btn = await subs_btn(services, lang=lang)
    await message.answer(context, reply_markup=btn)
    data.pop('service_categories')
    await state.update_data(data)
    await state.set_state(UserStates.service)


@router.message(UserStates.service, F.text)
async def service_state(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    lang = data['lang']

    await state.update_data(service=message.text)
    services = await search_services(user_id=user_id, service=message.text, lang=lang)
    if services['total_services']:
        city = languages[lang]['reply_button']['only_uzbekistan'] if services['user']['all_regions'] else \
            services['user'][
                'city']
        context = await pagination_context_maker(
            context=languages[lang]['find_text'].format(city, services['total_services'], services["services"][0]["service"]),
            data=services['services']
        )
        await message.answer("⏳", reply_markup=await start_command_btn(lang))
        btn = await service_pagination_btn(services['services'], 1, services['total_services'])
        await message.answer(context, reply_markup=btn)
        await state.set_state(None)
    else:
        context = languages[lang]['no_find_text']
        await message.answer(context)


@router.callback_query(Pagination.filter())
async def prev_page_callback(c: CallbackQuery, state: FSMContext):
    await c.answer()
    user_id = c.from_user.id
    page = int(c.data.split(':')[-1])
    data = await state.get_data()
    lang = data['lang']
    services = await search_services(user_id=user_id, service=data['service'], offset=page)
    city = languages[lang]['reply_button']['only_uzbekistan'] if services['user']['all_regions'] else services['user'][
        'city']
    context = await pagination_context_maker(
        context=languages[lang]['find_text'].format(city, services['total_services']),
        data=services['services']
    )
    if c.message.html_text != context.strip():
        btn = await service_pagination_btn(services['services'], page, services['total_services'])
        await c.message.edit_text(context, reply_markup=btn)


@router.callback_query(Staff.filter())
async def staff_callback(c: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data['lang']
    user_id = c.from_user.id
    stuff_id = int(c.data.split(":")[-1])
    staff_info = await stuff_service(stuff_id, lang)
    btn = await call_btn(lang, staff_info['phone_number'], stuff_id, 'service', user_id)
    price = staff_info['price'] if staff_info['price'] > 0 else languages[lang]['no_price_text']
    location_url = staff_info['location_url'] if staff_info['location_url'] else languages[lang]['no_location_url_text']
    context = languages[lang]['service_info_text'].format(
        staff_info['fullname'], staff_info['service'], staff_info['rating'], staff_info['comments'], price, staff_info['city'],
        staff_info['experience'], location_url, staff_info['description']
    )
    await c.message.answer(context, reply_markup=btn, disable_web_page_preview=True)


@router.callback_query(StaffComment.filter())
async def staff_comment_callback(c: CallbackQuery, state: FSMContext):
    await c.answer()
    data = await state.get_data()
    lang = data['lang']
    stuff_id = int(c.data.split(":")[-1])
    await state.update_data(
        text=c.message.html_text,
        btn=c.message.reply_markup
    )
    comments = await stuff_comments(stuff_id)
    if comments:
        await state.update_data(comments=comments, in_comment=0)
        btn = await stuff_comment_btn(len(comments))
        context = languages[lang]['comment_text'].format(comments[0]['tg_user'], comments[0]['comment'])
        await c.message.edit_text(context, reply_markup=btn)
    else:
        context = languages[lang]['no_comments_text']
        await c.answer(context, show_alert=True)
