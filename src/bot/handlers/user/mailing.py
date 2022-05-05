from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.config.loader import bot
from bot.services.db import user as user_db
from bot.states.mailing import Mailing


async def start_mailing(message: types.Message):
    user_id = message.from_user.id
    await bot.delete_message(
        chat_id=user_id,
        message_id=message.message_id
    )
    admins = await user_db.select_all_admins()
    a_list = [a.user_id for a in admins]
    if user_id in a_list:
        await bot.send_message(
            user_id,
            "Пришлите сообщение для рассылки"
        )
    await Mailing.waiting_for_message.set()


async def get_message(message: types.Message, state: FSMContext):
    if message.photo:
        caption = message.caption if message.caption else ""
        photo_id = message.photo[-1].file_id
        users = await user_db.select_all_users()
        u_list = [u.user_id for u in users]
        for user in u_list:
            try:
                await bot.send_photo(
                    chat_id=user,
                    photo=photo_id,
                    caption=caption,
                )
            except Exception as e:
                await bot.send_message(
                    chat_id=message.chat.id,
                    text=f"сообщение не доставлено пользователю {user}, причина - бот заблокирован им."
                )
    else:
        text = message.text
        users = await user_db.select_all_users()
        u_list = [u.user_id for u in users]
        for user in u_list:
            try:
                await bot.send_message(
                    chat_id=user,
                    text=text,
                )
            except Exception as e:
                await bot.send_message(
                    chat_id=message.chat.id,
                    text=f"сообщение не доставлено пользователю {user}, причина - бот заблокирован им."
                )
    await bot.send_message(
        chat_id=message.chat.id,
        text="Рассылка завершена"
    )
    await state.finish()
