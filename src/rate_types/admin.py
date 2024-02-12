from django.contrib import admin

from rate_types.models import RateType


class RateTypeAdmin(admin.ModelAdmin):
    # fieldsets = (
    #     (None, {"fields": ("email", "password")}),
    # )
    list_display = ("name", "energy_type")
    # list_filter = ("", )
    # search_fields = ("",)
    # ordering = ("",)


admin.site.register(RateType, RateTypeAdmin)
