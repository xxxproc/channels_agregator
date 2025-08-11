from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage
import redis.asyncio as r
from config import token

redis = r.from_url("redis://localhost:6379")
storage = RedisStorage(redis)

bot = Bot(token=token, default=DefaultBotProperties(parse_mode='HTML'))
dp = Dispatcher(storage=storage)