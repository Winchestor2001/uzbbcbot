from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage

from data import config

bot = Bot(token=config.BOT_TOKEN, parse_mode=ParseMode.HTML)
# storage = MemoryStorage()
storage = RedisStorage.from_url(f'redis://{config.REDIS_HOST}:{config.REDIS_PORT}/0')
dp = Dispatcher(storage=storage, user_data={})
