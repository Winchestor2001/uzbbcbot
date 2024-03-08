from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from telegram_bot.filters.user_filters import BtnLangCheck
from telegram_bot.states.AllStates import UserStates

router = Router()


@router.message(BtnLangCheck('service_text'))
async def service_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data['lang']
    # context = languages[lang]['location_text']
    # btn = await location_btn(lang)
    # await message.answer(context, reply_markup=btn)
    # await state.set_state(UserStates.location)


# @router.message(UserStates.location)
# async def location_state(message: Message, state: FSMContext):
#     data = await state.get_data()
#     lang = data['lang']
#     lat = message.location.latitude
#     lon = message.location.longitude
#     btn = await start_command_btn(lang)
#     services = await search_service_by_location(message.from_user.id, lat, lon)
#     loading = await message.answer("⏳", reply_markup=btn)
#     await loading.delete()
#     for item in services:
#         location = calc_distance(lat, lon, item['latitude'], item['longitude'])
#         context = languages[lang]['service_info_text'].format(
#             item['fullname'], item['professional'], item['price'], item['region'], location
#         )
#         btn = await service_btn(lang, item['phone_number'])
#         await message.answer(context, reply_markup=btn)
#
#     await state.set_state(None)
