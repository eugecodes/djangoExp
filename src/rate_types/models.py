from auditlog.registry import auditlog
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import StatusModel, TimeStampedModel

from common.choices import EnergyTypes
from rate_types.choices import RateTypeStatus


class RateType(StatusModel, TimeStampedModel, RateTypeStatus):
    name = models.CharField(max_length=256)
    energy_type = models.CharField(max_length=11, choices=EnergyTypes.ENERGY_TYPES)

    max_power = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    min_power = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    # commissions = relationship("Commission", back_populates="rate_type")
    # saving_studies = relationship("SavingStudy", back_populates="current_rate_type")

    class Meta:
        verbose_name = _("RateType")

    def __str__(self):
        return f"{self._meta.verbose_name}: {self.id} - {self.name}"


auditlog.register(RateType)
