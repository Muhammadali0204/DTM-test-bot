from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.client.default import DefaultBotProperties

from redis.asyncio import Redis

from app.data.config import settings



bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
storage = RedisStorage.from_url(settings.REDIS_URL)
dp = Dispatcher(storage=storage, bot=bot)
redis : Redis= None
temp_data = {}
