from django.apps import AppConfig

class {{ cookiecutter.app_name }}sConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "{{ cookiecutter.app_slug_plural }}"
