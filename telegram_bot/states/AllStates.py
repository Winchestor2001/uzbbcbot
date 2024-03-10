from aiogram.fsm.state import StatesGroup, State


class UserStates(StatesGroup):
    phone_number = State()
    search_service = State()
    region = State()
    city = State()
    service_category = State()
    service = State()
    product_category = State()
    product = State()

