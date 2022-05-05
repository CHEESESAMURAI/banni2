from aiogram import Dispatcher, types
from aiogram.dispatcher import filters

from bot.handlers.user import cleaner, setup_admin, create_user_disck, user_menu, discussion, admin_answer, mailing
from bot.states import AppendDiscussion
from bot.states.mailing import Mailing
from bot.states.setup_role import Role


def setup(dp: Dispatcher):
    # setup user roles
    dp.register_message_handler(setup_admin.setup_user_role, filters.Command("setup"))
    dp.register_message_handler(setup_admin.check_key, state=Role.secret_key)
    # set user chanel id
    dp.register_message_handler(
        setup_admin.update_chanel, lambda message: message.forward_from_chat
    )
    # handle commands
    dp.register_message_handler(
        create_user_disck.user_start, filters.CommandStart()
    )
    dp.register_message_handler(mailing.start_mailing, filters.Command("mailing"))
    dp.register_message_handler(mailing.get_message, content_types=types.ContentTypes.ANY,
                                state=Mailing.waiting_for_message)
    dp.register_message_handler(create_user_disck.send_menu, filters.Command("menu"))
    # admin answers
    dp.register_callback_query_handler(admin_answer.send_card, lambda call: call.data.startswith("card_"))
    dp.register_callback_query_handler(admin_answer.send_code, lambda call: call.data.startswith("code_"))
    dp.register_callback_query_handler(admin_answer.access_denied, lambda call: call.data.startswith("denied_"))
    dp.register_message_handler(
        admin_answer.answer_from_admin, lambda message: message.reply_to_message
    )
    # menu
    dp.register_message_handler(discussion.append_d, state=AppendDiscussion.sending)
    dp.register_message_handler(discussion.append_photo, content_types=types.ContentTypes.PHOTO,
                                state=AppendDiscussion.sending)
    dp.register_message_handler(discussion.append_photo, content_types=types.ContentTypes.DOCUMENT,
                                state=AppendDiscussion.sending)
    dp.register_callback_query_handler(user_menu.edit_menu, lambda call: call.data.startswith("act_"), state="*")
    dp.register_callback_query_handler(user_menu.back, lambda call: call.data == "back", state="*")
    dp.register_message_handler(cleaner.clean_s)
