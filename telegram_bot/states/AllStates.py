from aiogram.fsm.state import StatesGroup, State


class UserStates(StatesGroup):
    phone_number = State()
    verify_code = State()
    region = State()
    city = State()

