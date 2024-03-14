from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage

from core.settings import REDIS_HOST, REDIS_PORT
from data import config

bot = Bot(token=config.BOT_TOKEN, parse_mode=ParseMode.HTML)
# storage = MemoryStorage()
storage = RedisStorage.from_url(f'redis://{REDIS_HOST}:{REDIS_PORT}/0')
dp = Dispatcher(storage=storage, user_data={})
