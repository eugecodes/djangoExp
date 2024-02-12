from auditlog.registry import auditlog
from django.db import models
from django.db.models import CASCADE
from django.utils.translation import gettext_lazy as _
from model_utils.models import StatusModel, TimeStampedModel

from margins.choices import MarginStatus, MarginType


class Margin(StatusModel, TimeStampedModel, MarginStatus):
    type = models.CharField(max_length=13, choices=MarginType.MARGIN_TYPES)
    min_consumption = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    max_consumption = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    min_margin = models.DecimalField(max_digits=14, default=0, decimal_places=2)
    max_margin = models.DecimalField(max_digits=14, default=100, decimal_places=2)

    rate = models.ForeignKey("rates.Rate", on_delete=CASCADE, related_name="margin")

    class Meta:
        verbose_name = _("Margin")

    def __str__(self):
        return f"{self._meta.verbose_name}: {self.id}"


auditlog.register(Margin)
