from aiohttp import ClientSession
from data.config import API_URL
import logging

logger = logging.getLogger(__name__)


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


async def get_regions(lang: str):
    async with ClientSession() as session:
        params = {"lang": lang}
        async with session.get(f"{API_URL}/regions/", params=params) as response:
            if response.status == 200:
                return await response.json()
            else:
                return []


async def verify_user(user_id: int, phone_number: str):
    data = {"user_id": user_id, "phone_number": phone_number}
    async with ClientSession() as session:
        async with session.patch(f"{API_URL}/verify_user/", data=data) as response:
            if response.status == 200:
                return await response.json()
            else:
                return False


async def update_user_regions(user_id: int, city: str):
    data = {"user_id": user_id, "city": city}
    async with ClientSession() as session:
        async with session.patch(f"{API_URL}/verify_user/", data=data) as response:
            if response.status == 200:
                return await response.json()
            else:
                return False
            

async def get_user_info(user_id: int):
    async with ClientSession() as session:
        async with session.get(f"{API_URL}/user_info/{user_id}/") as response:
            if response.status == 200:
                return await response.json()
            else:
                return None


async def get_service_categories(lang: str):
    params = {"lang": lang}
    async with ClientSession() as session:
        async with session.get(f"{API_URL}/get_services/", params=params) as response:
            if response.status == 200:
                return await response.json()
            else:
                return []


async def search_services(user_id: int, service: str, lang: str, offset: int = 1):
    params = {'user_id': user_id, 'offset': offset, 'service': service, "lang": lang}
    async with ClientSession() as session:
        async with session.get(f"{API_URL}/search_services/", params=params) as response:
            if response.status == 200:
                return await response.json()
            else:
                return []


async def stuff_service(stuff_id: int, lang: str):
    params = {'stuff_id': stuff_id, "lang": lang}
    async with ClientSession() as session:
        async with session.get(f"{API_URL}/stuff_service/", params=params) as response:
            if response.status == 200:
                return await response.json()
            else:
                return []


async def stuff_comments(stuff_id: int):
    params = {'stuff_id': stuff_id}
    async with ClientSession() as session:
        async with session.get(f"{API_URL}/stuff_comments/", params=params) as response:
            if response.status == 200:
                return await response.json()
            else:
                return []


async def get_product_categories(lang: str):
    params = {"lang": lang}
    async with ClientSession() as session:
        async with session.get(f"{API_URL}/get_products/", params=params) as response:
            if response.status == 200:
                return await response.json()
            else:
                return []


async def search_products(user_id: int, product: str, lang: str, offset: int = 1):
    params = {'user_id': user_id, 'offset': offset, 'product': product, "lang": lang}
    async with ClientSession() as session:
        async with session.get(f"{API_URL}/search_products/", params=params) as response:
            if response.status == 200:
                return await response.json()
            else:
                return []


async def get_product_info(product_id: int):
    params = {'product_id': product_id}
    async with ClientSession() as session:
        async with session.get(f"{API_URL}/product_info/", params=params) as response:
            if response.status == 200:
                return await response.json()
            else:
                return []


async def product_comments(product_id: int):
    params = {'product_id': product_id}
    async with ClientSession() as session:
        async with session.get(f"{API_URL}/product_comments/", params=params) as response:
            if response.status == 200:
                return await response.json()
            else:
                return []


async def search_by_text(user_id: int, text: str):
    params = {'user_id': user_id, "q": text}
    async with ClientSession() as session:
        async with session.get(f"{API_URL}/search/", params=params) as response:
            if response.status == 200:
                return await response.json()
            else:
                return []


async def add_service_review(user_id: int, service_id: int, rating: int, comment: str):
    data = {'user_id': user_id, "service_id": service_id, "rating": rating, "comment": comment}
    async with ClientSession() as session:
        async with session.post(f"{API_URL}/stuff_comments/", data=data) as response:
            if response.status == 200:
                return await response.json()


async def add_product_review(user_id: int, product_id: int, rating: int, comment: str):
    data = {'user_id': user_id, "product_id": product_id, "rating": rating, "comment": comment}
    async with ClientSession() as session:
        async with session.post(f"{API_URL}/product_comments/", data=data) as response:
            if response.status == 200:
                return await response.json()
            

async def get_about_bot():
    async with ClientSession() as session:
        async with session.get(f"{API_URL}/about_bot/") as response:
            if response.status == 200:
                return await response.json()
            else:
                return []
            