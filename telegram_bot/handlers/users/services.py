from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from telegram_bot.filters.user_filters import BtnLangCheck
from telegram_bot.keyboards.default.user_btns import choose_service_category_btn, subs_btn, start_command_btn
from telegram_bot.keyboards.inline.user_btns import service_pagination_btn, Pagination
from telegram_bot.states.AllStates import UserStates
from telegram_bot.utils.api_connections import search_services, get_service_categories
from telegram_bot.utils.bot_context import languages
from telegram_bot.utils.usefull_functions import services_context_maker, get_services

router = Router()


@router.message(BtnLangCheck('service_text'))
async def service_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data['lang']

    service_categories = await get_service_categories()
    await state.update_data(service_categories=service_categories)
    context = languages[lang]['choose_service_category']
    btn = await choose_service_category_btn(lang, service_categories)
    await message.answer(context, reply_markup=btn)
    await state.set_state(UserStates.service_category)


@router.message(UserStates.service_category, F.text)
async def service_category_state(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data['lang']
    services = await get_services(
        obj=data['service_categories'],
        category=message.text
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
    services = await search_services(user_id=user_id, service=message.text)
    print(services)
    if services['total_services']:
        city = languages[lang]['reply_button']['only_uzbekistan'] if services['user']['all_regions'] else services['user'][
            'city']
        context = await services_context_maker(
            context=languages[lang]['services_text'].format(city, services['total_services']),
            data=services['services']
        )
        await message.answer("⏳", reply_markup=await start_command_btn(lang))
        btn = await service_pagination_btn(services['services'], 1, services['total_services'])
        await message.answer(context, reply_markup=btn)
        await state.set_state(None)
    else:
        context = languages[lang]['no_services_text']
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
    context = await services_context_maker(
        context=languages[lang]['services_text'].format(city, services['total_services']),
        data=services['services']
    )
    if c.message.html_text != context.strip():
        btn = await service_pagination_btn(services['services'], page, services['total_services'])
        await c.message.edit_text(context, reply_markup=btn)
