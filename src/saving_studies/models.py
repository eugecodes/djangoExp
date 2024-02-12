from decimal import Decimal

from auditlog.registry import auditlog
from django.db import models
from django.db.models import CASCADE
from django.utils.translation import gettext_lazy as _
from djmoney.models.fields import MoneyField
from model_utils.models import StatusModel, TimeStampedModel

from clients.choices import ClientTypes
from common.choices import EnergyTypes
from saving_studies.choices import SavingStudyStatus


class SavingStudy(StatusModel, TimeStampedModel, SavingStudyStatus):
    channel = models.ForeignKey(
        "channels.Channel", on_delete=CASCADE, null=False, blank=False
    )
    energy_type = models.CharField(max_length=11, choices=EnergyTypes.ENERGY_TYPES)

    is_existing_client = models.BooleanField(default=False)
    is_from_sips = models.BooleanField(default=False)
    is_compare_conditions = models.BooleanField(default=False)

    cups = models.CharField(max_length=124)

    analyzed_days = models.IntegerField(null=True, blank=True)
    current_marketer = models.CharField(max_length=124, null=True, blank=True)
    current_rate_type = models.ForeignKey(
        "rate_types.RateType",
        on_delete=CASCADE,
        null=True,
        blank=True,
        related_name="saving_studies",
    )

    # client data
    client_type = models.CharField(
        max_length=20, choices=ClientTypes.CLIENT_TYPES, null=True, blank=True
    )
    client_name = models.CharField(max_length=124, null=True, blank=True)
    client_nif = models.CharField(max_length=10, null=True, blank=True)

    # energy
    consumption_p1 = models.IntegerField(null=True, blank=True)
    consumption_p2 = models.IntegerField(null=True, blank=True)
    consumption_p3 = models.IntegerField(null=True, blank=True)
    consumption_p4 = models.IntegerField(null=True, blank=True)
    consumption_p5 = models.IntegerField(null=True, blank=True)
    consumption_p6 = models.IntegerField(null=True, blank=True)

    annual_consumption = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    energy_price_1 = MoneyField(max_digits=10, decimal_places=6, null=True, blank=True)
    energy_price_2 = MoneyField(max_digits=10, decimal_places=6, null=True, blank=True)
    energy_price_3 = MoneyField(max_digits=10, decimal_places=6, null=True, blank=True)
    energy_price_4 = MoneyField(max_digits=10, decimal_places=6, null=True, blank=True)
    energy_price_5 = MoneyField(max_digits=10, decimal_places=6, null=True, blank=True)
    energy_price_6 = MoneyField(max_digits=10, decimal_places=6, null=True, blank=True)

    # power
    power_1 = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    power_2 = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    power_3 = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    power_4 = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    power_5 = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    power_6 = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    power_price_1 = MoneyField(max_digits=10, decimal_places=6, null=True, blank=True)
    power_price_2 = MoneyField(max_digits=10, decimal_places=6, null=True, blank=True)
    power_price_3 = MoneyField(max_digits=10, decimal_places=6, null=True, blank=True)
    power_price_4 = MoneyField(max_digits=10, decimal_places=6, null=True, blank=True)
    power_price_5 = MoneyField(max_digits=10, decimal_places=6, null=True, blank=True)
    power_price_6 = MoneyField(max_digits=10, decimal_places=6, null=True, blank=True)

    fixed_price = MoneyField(max_digits=14, decimal_places=6, null=True, blank=True)
    other_cost_kwh = MoneyField(max_digits=14, decimal_places=6, null=True, blank=True)
    other_cost_percentage = models.DecimalField(
        max_digits=14, decimal_places=2, null=True, blank=True
    )
    other_cost_eur_month = MoneyField(
        max_digits=14, decimal_places=6, null=True, blank=True
    )

    # suggested_rates = relationship("SuggestedRate", back_populates="saving_study")
    # contract = relationship("Contract", back_populates="saving_study")

    @property
    def total_consumption(self) -> Decimal:
        if self.current_rate_type.energy_type == EnergyTypes.GAS:
            return self.consumption_p1 or Decimal("0.0")

        total_consumption = Decimal("0.0")
        for i in range(1, 7):
            if consumption := getattr(self, f"consumption_p{i}"):
                total_consumption += consumption

        return total_consumption

    class Meta:
        verbose_name = _("SavingStudy")

    def __str__(self):
        return f"{self._meta.verbose_name}: {self.id} - {self.cups}"


auditlog.register(SavingStudy)
