from aiogram import types, Router, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database import Database
from create_bot import bot


router = Router()


@router.callback_query(F.data == "my_channels")
async def get_my_channels(call: types.CallbackQuery):
    markup = InlineKeyboardBuilder()
    markup.row(types.InlineKeyboardButton(text="Главное меню", callback_data="main_menu"))
    ids = await Database.get_my_channels(call.from_user.id)
    if ids != []:
        for id in ids:
            channel = await bot.get_chat(id)
            channel_name = channel.title
            markup.row(types.InlineKeyboardButton(text=channel_name, callback_data=str(id)))
        await call.message.edit_text("Ваши каналы:", reply_markup=markup.as_markup())
    else:
        markup.row(types.InlineKeyboardButton(text="Добавить", callback_data="add_channel"))
        await call.message.edit_text("У вас еще нет каналов", reply_markup=markup.as_markup())