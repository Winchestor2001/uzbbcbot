import requests
from environs import Env
import json

env = Env()
env.read_env()

languages = {
    "uz": {
        "start_command": "👋 Assalomu aleykum",
        "set_lang_handler": "⚙️ Tilni tanlang:",
        "get_phone_number_handler": "☎️ Telefon raqamingizni yuboring",
        "choose_region_handler": "🌇 Viloyatni tanlang",
        "choose_city_handler": "🌇 Tumani tanlang",
        "verify_code_text": "🔢 Sms dagi kodni kiriting:",
        "wrong_code_text": "⚠️ Noto`g`ri kod",
        "profile_text": "🆔 <code>{}</code>\n👤 <b>{}</b>\n🌇 <b>{}</b>\n☎️ <code>{}</code>",
        "find_text": "<b>{}</b> bo`yicha <b>{}</b> ta {} topildi.\n\n",
        "service_info_text": "<b>Ism:</b> {}\n<b>Soxasi:</b> {}\n<b>Ball:</b> ⭐️{} ({})\n<b>Narxi:</b> {} UZS\n<b>Viloyati:</b> {}\n<b>Ish boshlanag sana:</b> {}\n📍 <a href='{}'>Manzil</a>\n\n{}",
        "product_info_text": "<b>Nomi:</b> {}\n<b>Mahsulot turi:</b> {}\n<b>Ball:</b> ⭐️{} ({})\n<b>Narxi:</b> {} - {} UZS\n<b>Viloyati:</b> {}\n📍 <a href='{}'>Manzil</a>\n\n{}",
        "choose_service_category": "Xizmat turini tanlang:",
        "choose_product_category": "Mahsulot tanlang:",
        "no_services_text": "Xizmat turi topilmadi",
        "no_product_text": "Mahsulot turi topilmadi",
        "comment_header": "Izohlar",
        "admin_text": "Bot Administratori: @username",
        "no_find_text": "Xech narsa topilmadi",
        "called_text": "<b>{}</b> da siz <b>{}</b> murojat qildiz.",
        "no_price_text": "Ko`rsatilmagan",
        "no_location_url_text": "Ko`rsatilmagan",
        "search_text": "✍️ Kamida 3ta belgi yozing:",
        "min_text": "⚠️ Eng kami 3 xarif bo`lishi lozim",
        "add_rating": "Baholang:",
        "add_commant": "Izoh yozing:",
        "review_added": "✅ Izoh saqlandi",

        "reply_button": {
            "service_text": "👷‍♂️ Xizmatlar",
            "product_text": "📦 Mahsulotlar",
            "about_text": "ℹ️ Bot Xaqida",
            "admin_text": "👤 Bot Admini",
            "phone_number_text": "📞 Telefon raqam",
            "profile_text": "💼 Profil",
            "edit_user_info": "⚙️ Malumotlarni o`zgartirish",
            "edit_language_text": "⚙️ Tilni o`zgartirish",
            "back_text": "🔙 Ortga",
            "location_text": "📍 Mening lokatsiyam",
            "call_text": "📞 {}",
            "only_uzbekistan": "📍 Uzbekiston bo`ylab",
            "only_cities": "📍 {} bo`ylab",
            "comment_text": "Izohlar",
            "called_text": "Izoh qoldirish",
            "no_called_text": "❌ Bekor qilish",
            "search_text": "🔎 Tez qidiruv",
        }
    },
    "ru": {
        "start_command": "👋 Здравствуйте",
        "set_lang_handler": "⚙️ Выберите язык:",
        "get_phone_number_handler": "☎️ Отправьте телефон немор",
        "choose_region_handler": "🌇 Выберите регион",
        "choose_city_handler": "🌇 Выберите город",
        "verify_code_text": "🔢 Введите смс код:",
        "wrong_code_text": "⚠️ Неверный смс код",
        "profile_text": "🆔 <code>{}</code>\n👤 <b>{}</b>\n🌇 <b>{}</b>\n☎️ <code>{}</code>",
        "find_text": "В <b>{}</b> найдено <b>{}</b> {}\n\n",
        "service_info_text": "<b>Имя:</b> {}\n<b>Профессия:</b> {}\n<b>Рейтинг:</b> ⭐️{} ({})\n<b>Цена:</b> {} UZS\n<b>Область:</b> {}\n<b>В этом сфере:</b> {}\n📍 <a href='{}'>Адрес</a>\n\n{}",
        "product_info_text": "<b>Название:</b> {}\n<b>Тип:</b> {}\n<b>Рейтинг:</b> ⭐️{} ({})\n<b>Цена:</b> {} - {} UZS\n<b>Область:</b> {}\n📍 <a href='{}'>Адрес</a>\n\n{}",
        "choose_service_category": "Выберите вид сервиса:",
        "choose_product_category": "Выберите продукт:",
        "no_services_text": "Не найдено сервисов",
        "no_products_text": "Не найдено продуктов",
        "comment_header": "Комментарии",
        "admin_text": "Администратор бота: @username",
        "no_find_text": "Ничего не найдено",
        "called_text": "В <b>{}</b> вы позвонили <b>{}</b>.",
        "no_price_text": "Не задано",
        "no_location_url_text": "Не задано",
        "search_text": "✍️ Напишите минимум 3 буквы:",
        "min_text": "⚠️ Напишите минимум 3 букв",
        "add_rating": "Отцените:",
        "add_commant": "Напишите отзыв:",
        "review_added": "✅ Отзыв отправлен",

        "reply_button": {
            "service_text": "👷‍♂️ Сервисы",
            "product_text": "📦 Продукты",
            "about_text": "ℹ️ О боте",
            "admin_text": "👤 Администратор",
            "phone_number_text": "📞 Номер телефона",
            "profile_text": "💼 Профиль",
            "edit_user_info": "⚙️ Изменить информацию",
            "edit_language_text": "⚙️ Изменить язык",
            "back_text": "🔙 Назад",
            "location_text": "📍 Моя локация",
            "call_text": "📞 {}",
            "only_uzbekistan": "📍 Весь Узбекистан",
            "only_cities": "📍 Весь {}",
            "comment_text": "Комментарии",
            "called_text": "Оставить комментарие",
            "no_called_text": "❌ Отменить",
            "search_text": "🔎 Быстрый поиск",
        }
    },
    "en": {
        "start_command": "👋 Hello",
        "set_lang_handler": "⚙️ Choose a language",
        "get_phone_number_handler": "☎️ Send your phone number",
        "choose_region_handler": "🌇 Choose region",
        "choose_city_handler": "🌇 Choose city",
        "verify_code_text": "🔢 Enter sms code:",
        "wrong_code_text": "⚠️ Sms code is incorrect",
        "profile_text": "🆔 <code>{}</code>\n👤 <b>{}</b>\n🌇 <b>{}</b>\n☎️ <code>{}</code>",
        "find_text": "In <b>{}</b> found <b>{}</b> {}\n\n",
        "service_info_text": "<b>Name:</b> {}\n<b>Professional:</b> {}\n<b>Rating:</b> ⭐️{}\n<b>Price:</b> {} UZS\n<b>Region:</b> {}\n<b>Since:</b> {}\n📍 <a href='{}'>Address</a>\n\n{}",
        "product_info_text": "<b>Name:</b> {}\n<b>Type:</b> {}\n<b>Rating:</b> ⭐️{}\n<b>Price:</b> {} - {} UZS\n<b>Region:</b> {}\n📍 <a href='{}'>Address</a>\n\n{}",
        "choose_service_category": "Choose service category:",
        "choose_product_category": "Choose product category:",
        "no_services_text": "No services",
        "no_products_text": "No products",
        "comment_header": "Comments",
        "admin_text": "Administrator: @username",
        "no_find_text": "No find",
        "called_text": "You called in <b>{}</b> to <b>{}</b>",
        "no_price_text": "not set",
        "no_location_url_text": "not set",
        "search_text": "✍️ Enter minimum 3 words:",
        "min_text": "⚠️ Minimum words is 3",
        "add_rating": "Grade:",
        "add_commant": "Write review:",
        "review_added": "✅ Review added",

        "reply_button": {
            "service_text": "👷‍♂️ Services",
            "product_text": "📦 Products",
            "about_text": "ℹ️ About",
            "admin_text": "👤 Admin",
            "phone_number_text": "📞 Phone number",
            "profile_text": "💼 Profile",
            "edit_user_info": "⚙️ Edit Info",
            "edit_language_text": "⚙️ Edit language",
            "back_text": "🔙 Back",
            "location_text": "📍 My location",
            "call_text": "📞 {}",
            "only_uzbekistan": "📍 Only Uzbekistan",
            "only_cities": "📍 Only {}",
            "comment_text": "Comments",
            "called_text": "Write comment",
            "no_called_text": "❌ Cancel",
            "search_text": "🔎 Fast Search",
        }
    },
}


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
