from aiogram import types

from bot.config.loader import bot
from bot.data import dict_data as dd
from bot.keyboards import inline as ik
from bot.data import text_data as td

async def edit_menu(call: types.CallbackQuery):
    action = call.data.replace("act_", "")
    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        text=dd.btn_text[action],
        message_id=call.message.message_id,
        reply_markup=await ik.back()
    )


async def back(call: types.CallbackQuery):
    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        text=td.MAIN_TEXT,
        message_id=call.message.message_id,
        reply_markup=await ik.get_user_menu()
    )
