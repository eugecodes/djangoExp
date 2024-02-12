from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from margins.models import Margin


class MarginAdmin(admin.ModelAdmin):
    # fieldsets = (
    #     (None, {"fields": ("email", "password")}),
    # )
    list_display = ("id", "created")
    # list_filter = ("", )
    # search_fields = ("",)
    # ordering = ("",)


admin.site.register(Margin, MarginAdmin)
