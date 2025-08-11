from aiogram import types, Router, F
from aiogram.utils.keyboard import InlineKeyboardMarkup
from database import Database
from create_bot import bot, redis
from filters import IsUserChannel

router = Router()

@router.callback_query(F.data == "del_channel")
async def del_channel(call: types.CallbackQuery):
    channel_id = await redis.get(f"channel_id:{call.from_user.id}")
    channel_id = channel_id.decode("utf-8")
    await Database.delete_channel(int(channel_id))

    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text="Главное меню", callback_data="main_menu")]
        ]
    )

    await call.message.edit_text("Канал успешно удален", reply_markup=markup)

@router.callback_query(IsUserChannel())
async def get_channel_info(call: types.CallbackQuery):
    await redis.set(f"channel_id:{call.from_user.id}", call.data)
    channel = await bot.get_chat(id)
    channel_name = channel.title
    channel_link = channel.invite_link
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text="Ссылка на канал", url=channel_link)],
            [types.InlineKeyboardButton(text="Удалить канал из агрегатора", callback_data="del_channel")],
            [types.InlineKeyboardButton(text="Главное меню", callback_data="main_menu")]
        ]
    )

    await call.message.edit_text(text=channel_name, reply_markup=markup)