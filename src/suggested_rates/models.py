from auditlog.registry import auditlog
from django.db import models
from django.db.models import CASCADE
from django.utils.translation import gettext_lazy as _
from djmoney.models.fields import MoneyField
from model_utils.models import StatusModel, TimeStampedModel

from margins.choices import MarginType
from rates.choices import PriceTypes
from suggested_rates.choices import SuggestedRateStatus


class SuggestedRate(StatusModel, TimeStampedModel, SuggestedRateStatus):
    is_selected = models.BooleanField(default=False)
    channel = models.ForeignKey(
        "channels.Channel", on_delete=CASCADE, null=False, blank=False
    )
    saving_study = models.ForeignKey(
        "saving_studies.SavingStudy", on_delete=CASCADE, related_name="suggested_rates"
    )

    marketer_name = models.CharField(max_length=256)
    has_contractual_commitment = models.BooleanField()

    duration = models.IntegerField()
    rate_name = models.CharField(max_length=256)
    is_full_renewable = models.BooleanField()
    has_net_metering = models.BooleanField()
    net_metering_value = MoneyField(max_digits=10, decimal_places=2)

    # margin
    profit_margin_type = models.CharField(
        max_length=13, choices=MarginType.MARGIN_TYPES
    )
    min_profit_margin = MoneyField(max_digits=14, decimal_places=6)
    max_profit_margin = MoneyField(max_digits=14, decimal_places=6)
    applied_profit_margin = MoneyField(max_digits=10, decimal_places=2)

    # rate
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
    price_type = models.CharField(max_length=11, choices=PriceTypes.PRICE_TYPES)

    # computed data
    final_cost = MoneyField(max_digits=10, decimal_places=2, null=True, blank=True)
    energy_cost = MoneyField(max_digits=10, decimal_places=2, null=True, blank=True)
    power_cost = MoneyField(max_digits=10, decimal_places=2, null=True, blank=True)
    fixed_cost = MoneyField(max_digits=10, decimal_places=2, null=True, blank=True)
    other_costs = MoneyField(max_digits=10, decimal_places=2, null=True, blank=True)
    ie_cost = MoneyField(max_digits=10, decimal_places=2, null=True, blank=True)
    ih_cost = MoneyField(max_digits=10, decimal_places=2, null=True, blank=True)
    iva_cost = MoneyField(max_digits=10, decimal_places=2, null=True, blank=True)

    total_commission = MoneyField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    theoretical_commission = MoneyField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    other_costs_commission = MoneyField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    saving_relative = MoneyField(max_digits=10, decimal_places=2, null=True, blank=True)
    saving_absolute = MoneyField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name = _("SuggestedRate")

    def __str__(self):
        return f"{self._meta.verbose_name}: {self.id}"


auditlog.register(SuggestedRate)
