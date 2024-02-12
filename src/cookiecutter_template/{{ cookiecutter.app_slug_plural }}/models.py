from auditlog.registry import auditlog
from django.db import models
from django.db.models import CASCADE
from django.utils.translation import gettext_lazy as _
from model_utils.models import StatusModel, TimeStampedModel

from {{ cookiecutter.app_slug_plural }}.choices import {{ cookiecutter.app_name }}Status


class {{ cookiecutter.app_name }}(
    StatusModel,
    TimeStampedModel,
    {{ cookiecutter.app_name }}Status
):
    name = models.CharField(max_length=256)

    class Meta:
        verbose_name = _("{{ cookiecutter.app_name }}")

    def __str__(self):
        return f"{self._meta.verbose_name}: {self.id} - {self.name}"


auditlog.register({{ cookiecutter.app_name }})
