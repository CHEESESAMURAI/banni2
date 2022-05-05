from aiogram import types

from bot.config.loader import bot
from usersupport.models import TelegramUser, UserDiscussion
from bot.services.db import user as user_db
from bot.services.db import user_discussion as ud_db
from bot.data import text_data as td


async def answer_from_admin(message: types.Message):
    user_id = int(message.reply_to_message.text.split("\n")[0])
    user: TelegramUser = await user_db.select_user(
        user_id=user_id
    )
    d: UserDiscussion = await ud_db.select_discussion(user=user)
    answer = message.text
    history = f"{d.history}\nA:{answer}"
    await ud_db.add_history(user=user, history=history)
    await bot.send_message(
        chat_id=user_id,
        text=answer,
    )



async def send_code(call: types.CallbackQuery):
    user_id = call.data.replace("code_", "")
    await send_mes(user_id, td.TEXT_ANSWER_2)
    await call.answer()

    user: TelegramUser = await user_db.select_user(
        user_id=user_id
    )
    d: UserDiscussion = await ud_db.select_discussion(user=user)
    admins = await user_db.select_all_admins()
    a_list = {a.chanel_id: a.chat_id for a in admins}
    mes_id = eval(d.mes_id)
    for admin in a_list:
        await bot.send_message(
            chat_id=a_list[admin],
            text=td.SUCCESS_MESSAGE_CODE,
            reply_to_message_id=mes_id[a_list[admin]]
        )

async def send_card(call: types.CallbackQuery):
    user_id = call.data.replace("card", "")
    await send_mes(user_id, td.TEXT_ANSWER_2)
    await call.answer()

    user: TelegramUser = await user_db.select_user(
        user_id=user_id
    )
    d: UserDiscussion = await ud_db.select_discussion(user=user)
    admins = await user_db.select_all_admins()
    a_list = {a.chanel_id: a.chat_id for a in admins}
    mes_id = eval(d.mes_id)
    for admin in a_list:
        await bot.send_message(
            chat_id=a_list[admin],
            text=td.SUCCESS_MESSAGE_CARD,
            reply_to_message_id=mes_id[a_list[admin]]
        )


async def access_denied(call: types.CallbackQuery):
    user_id = call.data.replace("denied_", "")
    await send_mes(user_id, td.TEXT_ANSWER_1)
    await call.answer()

    user: TelegramUser = await user_db.select_user(
        user_id=user_id
    )
    d: UserDiscussion = await ud_db.select_discussion(user=user)
    admins = await user_db.select_all_admins()
    a_list = {a.chanel_id: a.chat_id for a in admins}
    mes_id = eval(d.mes_id)
    for admin in a_list:
        await bot.send_message(
            chat_id=a_list[admin],
            text=td.SUCCESS_MESSAGE_CANCEL,
            reply_to_message_id=mes_id[a_list[admin]]
        )


async def send_mes(user_id, text):
    user: TelegramUser = await user_db.select_user(
        user_id=user_id
    )
    d: UserDiscussion = await ud_db.select_discussion(user=user)
    history = f"{d.history}\nA:{text}"
    await ud_db.add_history(user=user, history=history)
    await bot.send_message(
        chat_id=user_id,
        text=text
    )
