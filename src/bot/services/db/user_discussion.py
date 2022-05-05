from usersupport.models import UserDiscussion, TelegramUser
from asgiref.sync import sync_to_async


@sync_to_async
def select_discussion(user):
    return UserDiscussion.objects.filter(user=user).first()


@sync_to_async
def select_discussion_by_id(user, pk):
    return UserDiscussion.objects.filter(user=user, pk=pk).first()


@sync_to_async
def add_discussion(user: TelegramUser, mes_id):
    # try:
    return UserDiscussion(user=user, mes_id=mes_id).save()
    # except Exception:
    #     return select_question(user=user)


@sync_to_async
def add_history(user, history):
    return UserDiscussion.objects.filter(user=user).update(history=f"{history}")


@sync_to_async
def add_mes_id(user, pk, mes_id):
    return UserDiscussion.objects.filter(user=user, pk=pk).update(mes_id=mes_id)
