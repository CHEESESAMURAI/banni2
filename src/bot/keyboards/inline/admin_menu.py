from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

__all__ = [
    "get_admin_menu"
]


async def get_admin_menu(user_id):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(text="💳", callback_data=f"card_{user_id}"),
        InlineKeyboardButton(text="🎁", callback_data=f"code_{user_id}"),
        InlineKeyboardButton(text="❌", callback_data=f"denied_{user_id}"),
    )
    return keyboard
