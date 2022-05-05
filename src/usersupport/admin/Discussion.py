from django.contrib import admin

from ..models import UserDiscussion


class DiscussionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "history",
        "mes_id",
    )


# Register your models here.
admin.site.register(UserDiscussion, DiscussionAdmin)
