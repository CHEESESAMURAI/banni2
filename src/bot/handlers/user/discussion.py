from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.config.loader import bot, user_data
from bot.handlers.user.create_user_disck import send_menu
from usersupport.models import UserDiscussion, TelegramUser
from bot.services.db import user as user_db
from bot.services.db import user_discussion as ud_db
from bot.keyboards import inline as ik


async def append_d(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    text = message.text
    if text == "/menu":
        await send_menu(message)
        return
    user: TelegramUser = await user_db.select_user(
        user_id=user_id
    )
    user_discussion: UserDiscussion = await ud_db.select_discussion(
        user=user,
    )
    history = f"{user_discussion.history if user_discussion.history else ''}\n{'U: ' + text}"
    await ud_db.add_history(user=user, history=history)
    admins = await user_db.select_all_admins()
    a_list = {a.chanel_id: a.chat_id for a in admins}
    mes_id = eval(user_discussion.mes_id)
    for admin in a_list:
        try:
            await bot.edit_message_reply_markup(
                chat_id=a_list[admin],
                message_id=user_data[a_list[admin]],
                reply_markup=None
            )
        except:
            pass
        mes = await bot.send_message(
            chat_id=a_list[admin],
            text=text,
            reply_to_message_id=mes_id[a_list[admin]],
            reply_markup=await ik.get_admin_menu(user_id)
        )
        user_data[a_list[admin]] = mes.message_id


async def append_photo(message: types.Message):
    user_id = message.from_user.id
    text = message.caption if message.caption else ""
    user: TelegramUser = await user_db.select_user(
        user_id=user_id
    )
    user_discussion: UserDiscussion = await ud_db.select_discussion(
        user=user,
    )
    history = f"{user_discussion.history if user_discussion.history else ''}\nU: Фото от пользователя с подписью: {text}"
    await ud_db.add_history(user=user, history=history)
    admins = await user_db.select_all_admins()
    a_list = {a.chanel_id: a.chat_id for a in admins}
    mes_id = eval(user_discussion.mes_id)
    for admin in a_list:
        try:
            photo_id = message.photo[-1].file_id
            await del_kb(a_list[admin])
            mes = await bot.send_photo(
                chat_id=a_list[admin],
                photo=photo_id,
                caption=text,
                reply_to_message_id=mes_id[a_list[admin]],
                reply_markup=await ik.get_admin_menu(user_id)
            )
            await del_kb(a_list[admin])
        except:
            await del_kb(a_list[admin])
            mes = await bot.send_document(
                chat_id=a_list[admin],
                document=message.document.file_id,
                caption=text,
                reply_to_message_id=mes_id[a_list[admin]],
                reply_markup=await ik.get_admin_menu(user_id))
            await del_kb(a_list[admin])
        user_data[a_list[admin]] = mes.message_id

async def del_kb(user_id):
    try:
        await bot.edit_message_reply_markup(
            chat_id=user_id,
            message_id=user_data[user_id],
            reply_markup=None
        )
    except:
        pass
