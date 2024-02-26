from aiohttp import ClientSession
from data.config import API_URL


async def add_user(user_id: int, username: str):
    data = {"user_id": user_id, "username": username}
    async with ClientSession() as session:
        async with session.post(f"{API_URL}/add_user/", data=data) as response:
            if response.status in [200, 201]:
                return await response.json()
            else:
                return False


async def get_user_language(user_id: int):
    async with ClientSession() as session:
        async with session.get(f"{API_URL}/user_lang/{user_id}/") as response:
            if response.status == 200:
                return await response.json()
            else:
                return None


async def update_user_language(user_id: int, language: str):
    data = {"language": language}
    async with ClientSession() as session:
        async with session.patch(f"{API_URL}/user_lang/{user_id}/", data=data) as response:
            if response.status == 200:
                return await response.json()
            else:
                return None


async def send_verify_code(user_id: int, phone_number: str):
    data = {"user_id": user_id, "phone_number": phone_number}
    async with ClientSession() as session:
        async with session.post(f"{API_URL}/send_verify/", data=data) as response:
            if response.status == 201:
                return await response.json()
            else:
                return False


async def get_regions():
    async with ClientSession() as session:
        async with session.get(f"{API_URL}/regions/") as response:
            if response.status == 200:
                return await response.json()
            else:
                return []
