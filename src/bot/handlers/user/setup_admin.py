from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

from bot.config.config import ADMIN_SECRET_KEY
from bot.config.loader import bot
from bot.keyboards.reply.setup_role import break_role_keyboard
from bot.states.setup_role import Role
from bot.services.db import user as user_db

__all__ = [
    "setup_user_role",
    "check_key",
    "update_chanel"
]


async def setup_user_role(message: types.Message):
    await bot.send_message(
        chat_id=message.chat.id,
        text="Введите секретный ключ",
        reply_markup=break_role_keyboard,
    )
    await Role.secret_key.set()


async def check_key(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    secret_key = message.text
    if secret_key == ADMIN_SECRET_KEY:
        await user_db.add_user_with_role(
            user_id=user_id,
            name=message.from_user.first_name,
            role="администратор",
            chat_id=message.chat.id,
        )
        await state.finish()
        await bot.send_message(
            chat_id=message.chat.id,
            text=f"Вы успешно авторизированы как администратор",
            reply_markup=ReplyKeyboardRemove(),
        )
    elif secret_key == "Отмена":
        await state.finish()
        await bot.send_message(
            chat_id=message.chat.id,
            text="Действия отменены",
            reply_markup=ReplyKeyboardRemove(),
        )
    else:
        await bot.send_message(
            chat_id=message.chat.id,
            text="Введенный ключ не соответсвует ожидаемому, попробуйте заново или нажмите на кнопку",
            reply_markup=break_role_keyboard,
        )


async def update_chanel(message: types.Message):
    chat_id = message.chat.id
    chanel_id = message.forward_from_chat.id
    await user_db.update_chanel_id(chat_id=chat_id, chanel_id=chanel_id)
