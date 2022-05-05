from usersupport.models import TelegramUser
from asgiref.sync import sync_to_async


@sync_to_async
def select_user(user_id) -> TelegramUser:
    user = TelegramUser.objects.filter(user_id=user_id).first()
    return user


@sync_to_async
def add_user(user_id, name, second_name, username, role, ):
    try:
        return TelegramUser(
            user_id=int(user_id), name=name, second_name=second_name, username=username, user_role=role,
        ).save()
    except Exception:
        return select_user(int(user_id))


@sync_to_async
def add_user_with_role(user_id, name, role, chat_id):
    try:
        return TelegramUser(
            user_id=int(user_id),
            name=name,
            user_role=role,
            chat_id=chat_id,
        ).save()
    except Exception:
        return select_user(int(user_id))


@sync_to_async
def update_chanel_id(chat_id, chanel_id):
    return TelegramUser.objects.filter(chat_id=chat_id).update(chanel_id=chanel_id)


@sync_to_async
def select_all_admins():
    return TelegramUser.objects.filter(user_role="администратор").all()


@sync_to_async
def select_all_users():
    return TelegramUser.objects.filter(user_role="пользователь").all()
