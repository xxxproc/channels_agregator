from aiogram import types, Router, F
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardMarkup

router = Router()

def menu_kb():
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text="Добавить канал", callback_data="add_channel")],
            [types.InlineKeyboardButton(text="Мои каналы", callback_data="my_channels")]
        ]
    )
    return markup

@router.message(CommandStart)
async def start_command(msg: types.Message):
    await msg.answer("Привет!\n\n"
                        "Чтобы добавить канал в агрегатор, нужно добавить бота в "
                        "администраторы, а затем перекинуть любой пост"
                        "из своего канала сюда(на канале должно быть >150"
                        "подписчиков)", reply_markup=menu_kb())

@router.callback_query(F.data == "main_menu")
async def main_menu(call: types.CallbackQuery):
    await call.message.edit_text("Привет!\n\n"
                             "Чтобы добавить канал в агрегатор, нужно добавить бота в "
                             "администраторы, а затем перекинуть любой пост"
                             "из своего канала сюда(на канале должно быть >150"
                             "подписчиков)", reply_markup=menu_kb())