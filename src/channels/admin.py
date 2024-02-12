from django.contrib import admin
from guardian.admin import GuardedModelAdmin

from channels.models import Channel


class ChannelAdmin(GuardedModelAdmin):
    list_display = ("id", "name")


admin.site.register(Channel, ChannelAdmin)
