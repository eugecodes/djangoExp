from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from suggested_rates.models import SuggestedRate


class SuggestedRateAdmin(admin.ModelAdmin):
    # fieldsets = (
    #     (None, {"fields": ("email", "password")}),
    # )
    list_display = ("id", "created")
    # list_filter = ("", )
    # search_fields = ("",)
    # ordering = ("",)


admin.site.register(SuggestedRate, SuggestedRateAdmin)
