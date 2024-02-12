from auditlog.registry import auditlog
from django.db import models
from django.db.models import CASCADE, JSONField
from django.utils.translation import gettext_lazy as _
from djmoney.models.fields import MoneyField
from model_utils.models import StatusModel, TimeStampedModel

from common.choices import EnergyTypes
from rates.choices import RateStatus, PriceTypes


class Rate(StatusModel, TimeStampedModel, RateStatus):
    name = models.CharField(max_length=256, unique=True)
    energy_type = models.CharField(max_length=11, choices=EnergyTypes.ENERGY_TYPES)
    price_type = models.CharField(max_length=11, choices=PriceTypes.PRICE_TYPES)

    client_types = JSONField("ClientTypes")

    max_power = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    min_power = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    min_consumption = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    max_consumption = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    energy_price_1 = MoneyField(max_digits=14, decimal_places=6, null=True, blank=True)
    energy_price_2 = MoneyField(max_digits=14, decimal_places=6, null=True, blank=True)
    energy_price_3 = MoneyField(max_digits=14, decimal_places=6, null=True, blank=True)
    energy_price_4 = MoneyField(max_digits=14, decimal_places=6, null=True, blank=True)
    energy_price_5 = MoneyField(max_digits=14, decimal_places=6, null=True, blank=True)
    energy_price_6 = MoneyField(max_digits=14, decimal_places=6, null=True, blank=True)

    power_price_1 = MoneyField(max_digits=14, decimal_places=6, null=True, blank=True)
    power_price_2 = MoneyField(max_digits=14, decimal_places=6, null=True, blank=True)
    power_price_3 = MoneyField(max_digits=14, decimal_places=6, null=True, blank=True)
    power_price_4 = MoneyField(max_digits=14, decimal_places=6, null=True, blank=True)
    power_price_5 = MoneyField(max_digits=14, decimal_places=6, null=True, blank=True)
    power_price_6 = MoneyField(max_digits=14, decimal_places=6, null=True, blank=True)

    fixed_term_price = MoneyField(
        max_digits=14, decimal_places=6, null=True, blank=True
    )

    permanency = models.BooleanField()
    length = models.IntegerField()
    is_full_renewable = models.BooleanField(null=True, blank=True)
    compensation_surplus = models.BooleanField(null=True, blank=True)
    compensation_surplus_value = MoneyField(
        max_digits=14, decimal_places=6, null=True, blank=True
    )

    rate_type = models.ForeignKey(
        "rate_types.RateType", on_delete=CASCADE, related_name="rates"
    )
    marketer = models.ForeignKey(
        "marketers.Marketer", on_delete=CASCADE, related_name="rates"
    )
    commission = models.ForeignKey(
        "commissions.Commission",
        on_delete=CASCADE,
        related_name="rates",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("Rate")

    def __str__(self):
        return f"{self._meta.verbose_name}: {self.id} - {self.name}"


auditlog.register(Rate)
