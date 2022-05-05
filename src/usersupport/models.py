from django.db import models


# Create your models here.
class TimeBasedModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(auto_now=True)


class TelegramUser(TimeBasedModel):
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    id = models.AutoField(primary_key=True)
    user_id = models.BigIntegerField(unique=True, verbose_name="UserID")
    name = models.CharField(max_length=255, verbose_name="UserName")
    second_name = models.CharField(max_length=255, verbose_name="SirName", default="")
    username = models.CharField(max_length=255, verbose_name="username", default="")
    user_role = models.CharField(max_length=255, verbose_name="Роль")
    chat_id = models.BigIntegerField(verbose_name="Чат пользователя", default=0)
    chanel_id = models.BigIntegerField(verbose_name="Канал пользователя", default=0)


class UserDiscussion(TimeBasedModel):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        TelegramUser, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    history = models.CharField(
        max_length=1000000, verbose_name="История вопроса", null=True
    )
    mes_id = models.CharField(max_length=20000, unique=False, default="")
