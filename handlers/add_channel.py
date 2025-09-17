from aiogram import types, Router, F
from aiogram.types import ChatMemberAdministrator
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardBuilder
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from database import Database
from create_bot import bot
from config import link_to_bot


router = Router()


class add_channel(StatesGroup):
    link = State()

@router.callback_query(F.data == "add_channel")
async def start_command(call: types.CallbackQuery, state: FSMContext):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text="Добавить бота", url=f"{link_to_bot}?startchannel&admin")],
            [types.InlineKeyboardButton(text="Отмена", callback_data="cancel")]
        ]
    )
    await call.message.edit_text(
        text="Добавь бота в канал с правами администратора, а затем перешли пост из канала сюда(помни, что нужно >150 подписчиков)",
        reply_markup=markup)
    await state.set_state(add_channel.link)


@router.message(F.forward_from_chat, add_channel.link)
async def adding_channel(message: types.Message, state: FSMContext):
    if message.forward_from_chat.type == "channel":
        channel_id = message.forward_from_chat.id
        bot_id = await bot.get_me()
        bot_id = bot_id.id
        bot_status = await bot.get_chat_member(channel_id, bot_id)

        if isinstance(bot_status, ChatMemberAdministrator):
            count = await bot.get_chat_member_count(chat_id=channel_id)
            if count >= 150:
                if await Database.if_channel_added(channel_id):
                    await message.answer("Данный канал уже добавлен\n"
                                         "Отмени запрос или добавь другой канал")
                else:
                    await Database.add_channel(message.from_user.id, channel_id)

                    markup = InlineKeyboardBuilder()
                    ids = await Database.get_my_channels(message.from_user.id)
                    for id in ids:
                        channel = await bot.get_chat(id)
                        channel_name = channel.title
                        markup.row(types.InlineKeyboardButton(text=channel_name, callback_data=str(id)))

                    markup.row(types.InlineKeyboardButton(text="Главное меню", callback_data="main_menu"))

                    await message.answer("Ваш канал успешно добавлен!\n\n"
                                         "Список ваших каналов:", reply_markup=markup.as_markup())
                    await state.clear()
            else:
                await message.answer("Прости, но твой канал не подходит под условия агреггатора")
                await state.clear()
        else:
            await message.answer("Бот не является администратором канала")
    else:
        await message.answer("Пожалуйста, перешлите сообщение из вашего канала")
        await message.delete()

@router.callback_query(F.data == "cancel")
async def cancel(call: types.CallbackQuery, state: FSMContext):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text="Главное меню", callback_data="main_menu")]
        ]
    )
    await call.message.edit_text("Успешно отменено", reply_markup=markup)
    await state.clear()