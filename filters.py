from aiogram.filters import BaseFilter
from database import Database
from aiogram.types import CallbackQuery

class IsUserChannel(BaseFilter):
    async def __call__(self, call: CallbackQuery) -> bool:
        ids = await Database.get_channels()
        for id in ids:
            if str(id) == call.data:
                return True
        return False