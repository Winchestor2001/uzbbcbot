from aiogram import types
from utils.api_connections import add_user


# class IsActiveFilter(BoundFilter):
#     async def check(self, message: types.Message):
#         user_data = await add_user(
#             user_id=message.from_user.id,
#             username=message.from_user.username
#         )
#         return user_data and user_data.get('is_active', False)
