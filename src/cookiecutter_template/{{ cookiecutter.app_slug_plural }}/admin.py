from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from {{ cookiecutter.app_slug_plural }}.models import {{ cookiecutter.app_name }}


class {{ cookiecutter.app_name }}Admin(admin.ModelAdmin):
    # fieldsets = (
    #     (None, {"fields": ("email", "password")}),
    # )
    list_display = ("id", "created")
    # list_filter = ("", )
    # search_fields = ("",)
    # ordering = ("",)


admin.site.register({{ cookiecutter.app_name }}, {{ cookiecutter.app_name }}Admin)
