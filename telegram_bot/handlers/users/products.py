from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from filters.user_filters import BtnLangCheck
from keyboards.default.user_btns import choose_category_btn, subs_btn, start_command_btn
from keyboards.inline.user_btns import product_pagination_btn, Product, call_btn, ProductComment, \
    product_comment_btn
from states.AllStates import UserStates
from utils.api_connections import get_product_categories, search_products, get_product_info, \
    product_comments
from utils.bot_context import languages
from utils.usefull_functions import get_sub_categories, pagination_context_maker

router = Router()


@router.message(BtnLangCheck('product_text'))
async def product_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data['lang']

    product_categories = await get_product_categories()
    await state.update_data(product_categories=product_categories)
    context = languages[lang]['choose_product_category']
    btn = await choose_category_btn(lang, product_categories)
    await message.answer(context, reply_markup=btn)
    await state.set_state(UserStates.product_category)


@router.message(UserStates.product_category, F.text)
async def product_category_state(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data['lang']
    services = await get_sub_categories(
        obj=data['product_categories'],
        category=message.text,
        key='products'
    )
    context = languages[lang]['choose_product_category']
    btn = await subs_btn(services, lang=lang)
    await message.answer(context, reply_markup=btn)
    data.pop('product_categories')
    await state.update_data(data)
    await state.set_state(UserStates.product)


@router.message(UserStates.product, F.text)
async def product_state(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    lang = data['lang']

    await state.update_data(service=message.text)
    products = await search_products(user_id=user_id, product=message.text)
    if products['total_products']:
        city = languages[lang]['reply_button']['only_uzbekistan'] if products['user']['all_regions'] else \
        products['user'][
            'city']
        context = await pagination_context_maker(
            context=languages[lang]['find_text'].format(city, products['total_products']),
            data=products['products']
        )
        await message.answer("⏳", reply_markup=await start_command_btn(lang))
        btn = await product_pagination_btn(products['products'], 1, products['total_products'])
        await message.answer(context, reply_markup=btn)
        await state.set_state(None)
    else:
        context = languages[lang]['no_products_text']
        await message.answer(context)


@router.callback_query(Product.filter())
async def staff_callback(c: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data['lang']
    product_id = int(c.data.split(":")[-1])
    product_info = await get_product_info(product_id)
    btn = await call_btn(lang, product_info['phone_number'], product_id, 'product')
    context = languages[lang]['product_info_text'].format(
        product_info['fullname'], product_info['product'], product_info['rating'], product_info['from_price'],
        product_info['to_price'], product_info['city'], product_info['location_url'], product_info['description']
    )
    await c.message.answer(context, reply_markup=btn, disable_web_page_preview=True)


@router.callback_query(ProductComment.filter())
async def product_comment_callback(c: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data['lang']
    product_id = int(c.data.split(":")[-1])
    await state.update_data(
        text=c.message.html_text,
        btn=c.message.reply_markup
    )
    comments = await product_comments(product_id)
    if comments:
        await state.update_data(comments=comments, in_comment=0)
        btn = await product_comment_btn(len(comments))
        context = languages[lang]['comment_text'].format(comments[0]['tg_user'], comments[0]['comment'])
        await c.message.edit_text(context, reply_markup=btn)
    else:
        context = languages[lang]['no_comments_text']
        await c.answer(context, show_alert=True)


