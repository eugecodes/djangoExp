from auditlog.registry import auditlog
from django.db import models
from django.db.models import CASCADE
from django.utils.translation import gettext_lazy as _
from djmoney.models.fields import MoneyField
from model_utils.models import StatusModel, TimeStampedModel

from common.choices import EnergyTypes
from common.mixins import BankDataMixin
from supply_points.choices import SupplyPointStatus, CounterType, OwnerType


class SupplyPoint(StatusModel, TimeStampedModel, SupplyPointStatus, BankDataMixin):
    channel = models.ForeignKey(
        "channels.Channel",
        on_delete=CASCADE,
        null=False,
        blank=False,
        related_name="supply_points",
    )
    client = models.ForeignKey(
        "clients.Client",
        on_delete=CASCADE,
        null=False,
        blank=False,
        related_name="supply_points",
    )
    energy_type = models.CharField(max_length=11, choices=EnergyTypes.ENERGY_TYPES)
    cups = models.CharField(max_length=124)
    alias = models.CharField(max_length=128, null=True)

    address = models.ForeignKey(
        "addresses.Address",
        on_delete=CASCADE,
        null=False,
        blank=False,
        related_name="supply_points",
    )

    # Technical information
    is_renewable = models.BooleanField(default=False)
    max_available_power = models.IntegerField(null=True, blank=True)
    voltage = models.IntegerField(null=True, blank=True)

    # Counter
    counter_type = models.CharField(max_length=11, choices=CounterType.TYPES)
    counter_property = models.CharField(max_length=11, choices=OwnerType.TYPES)
    counter_price = MoneyField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = _("SupplyPoint")
        unique_together = (("channel", "cups"),)

    def __str__(self):
        return f"{self._meta.verbose_name}: {self.id} - {self.cups}"


auditlog.register(SupplyPoint)
