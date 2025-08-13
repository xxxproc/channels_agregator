from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message
from datetime import datetime, timedelta
from create_bot import redis

class AntiFloodMw(BaseMiddleware):
    def __init__(
            self, 
            rate_limit: int = 10, 
            time_interval: timedelta = timedelta(seconds=10)):
        self.rate_limit = rate_limit
        self.time_interval = time_interval

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        
        user_id = event.from_user.id
        now = datetime.now().isoformat()

        await redis.lpush(f"flood:{user_id}", now)
        await redis.ltrim(f"flood:{user_id}", 0, self.rate_limit - 1)
        timestamps = await redis.lrange(f"flood:{user_id}", 0, -1)
        timestamps = [datetime.fromisoformat(i.decode("utf-8")) for i in timestamps]

        if len(timestamps) >= self.rate_limit and timestamps[0] - timestamps[-1] <= self.time_interval:
            return

        await redis.expire(f"flood:{user_id}", self.time_interval)

        return await handler(event, data)