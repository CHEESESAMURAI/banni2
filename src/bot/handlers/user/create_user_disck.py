from aiogram import types

from bot.config.loader import bot
from bot.services.db import user as user_db
from bot.services.db import user_discussion as ud_db
from bot.states.discussion import AppendDiscussion
from bot.states.mailing import Mailing
from usersupport.models import TelegramUser
from bot.data import text_data as td
from bot.keyboards import inline as ik


async def user_start(message: types.Message):
    user_id = message.from_user.id
    admins = await user_db.select_all_admins()
    a_list = [a.user_id for a in admins]
    if user_id in a_list:
        await bot.delete_message(
            chat_id=user_id,
            message_id=message.message_id
        )
        await bot.send_message(
            chat_id=user_id,
            text="Напишите /mailing, чтобы начать рассылку"
        )
        return
    name = message.from_user.first_name
    second_name = message.from_user.last_name if message.from_user.last_name else ""
    username = message.from_user.username if message.from_user.username else "username отсутствует"
    await user_db.add_user(
        user_id=user_id,
        name=name,
        second_name=second_name,
        username=username,
        role="пользователь"
    )
    user = await user_db.select_user(user_id=user_id)
    admins = await user_db.select_all_admins()
    a_list = {a.chanel_id: a.chat_id for a in admins}
    sent_q_id_dict = {}
    for admin in a_list:
        m = await bot.send_message(chat_id=a_list[admin], text=".")
        await bot.send_message(
            chat_id=admin,
            text=f"{user_id}\nПользователь, {name} {second_name}\n@{username}",
        )
        sent_q_id_dict[a_list[admin]] = m.message_id + 1
        await bot.delete_message(chat_id=a_list[admin], message_id=m.message_id)

    mes_id = str(sent_q_id_dict)
    d = await ud_db.add_discussion(user=user, mes_id=mes_id)
    # await ud_db.add_mes_id(user=user, pk=user.id, mes_id=mes_id)
    await AppendDiscussion.sending.set()
    await send_menu(message)


async def send_menu(message: types.Message):
    await bot.delete_message(
        chat_id=message.from_user.id,
        message_id=message.message_id
    )
    mes = await bot.send_message(
        chat_id=message.from_user.id,
        text=td.MAIN_TEXT,
        reply_markup=await ik.get_user_menu()
    )
