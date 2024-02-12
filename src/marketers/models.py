from auditlog.registry import auditlog
from django.db import models
from django.db.models import CASCADE
from django.utils.translation import gettext_lazy as _
from djmoney.models.fields import MoneyField
from model_utils.models import StatusModel, TimeStampedModel

from marketers.choices import MarketerStatus


class Marketer(StatusModel, TimeStampedModel, MarketerStatus):
    name = models.CharField(max_length=64)
    fiscal_name = models.CharField(max_length=64, unique=True)
    cif = models.CharField(max_length=9, unique=True)

    email = models.EmailField(null=True, blank=True)
    fee = MoneyField(max_digits=14, decimal_places=6, null=True, blank=True)
    max_consume = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )

    address = models.ForeignKey(
        "addresses.Address",
        on_delete=CASCADE,
        null=True,
        blank=True,
        related_name="marketers",
    )

    # consume_range_datetime = Column(DateTime)
    # # TODO: Remove it
    # surplus_price = Column(Numeric(14, 6))

    class Meta:
        verbose_name = _("Marketer")

    def __str__(self):
        return f"{self._meta.verbose_name}: {self.id} - {self.name}"


auditlog.register(Marketer)
