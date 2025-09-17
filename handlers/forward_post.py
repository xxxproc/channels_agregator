from aiogram import types, Router
from collections import defaultdict
import asyncio
from database import Database
from config import id_of_main_channel


router = Router()


media_groups = defaultdict(list)
media_group_timeouts = {}

@router.channel_post()
async def forward_post(message: types.Message):
    channel_ids = await Database.get_channels()
    if message.chat.id not in channel_ids:
        return

    content = message.text or message.caption
    normalized = (content or "").lower().replace(" ", "")
    passes_filter = len(normalized) >= 50

    if message.media_group_id:
        media_groups[message.media_group_id].append((message, passes_filter))
        if message.media_group_id not in media_group_timeouts:
            media_group_timeouts[message.media_group_id] = asyncio.create_task(
                forward_first_from_album(message.media_group_id)
            )
    else:
        if passes_filter or not content:
            await message.forward(chat_id=id_of_main_channel)

async def forward_first_from_album(group_id):
    await asyncio.sleep(2.5)

    messages = media_groups.pop(group_id, [])
    media_group_timeouts.pop(group_id, None)

    messages.sort(key=lambda x: x[0].message_id)
    first_message, passes_filter = messages[0]

    if passes_filter:
        await first_message.forward(chat_id=id_of_main_channel)
