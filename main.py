import asyncio
from create_bot import dp, bot
from database import create_table
import logging

from handlers.start_command import router as start_command
from handlers.add_channel import router as add_channel_router
from handlers.forward_post import router as forward_router
from handlers.get_my_channels import router as get_channels_router
from handlers.del_channel import router as del_channel_router

from handlers.errors.base import router as error_router

async def main():
    await create_table()

    dp.include_router(add_channel_router)
    dp.include_router(start_command)

    dp.include_router(forward_router)
    dp.include_router(get_channels_router)
    dp.include_router(del_channel_router)

    dp.include_router(error_router)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
