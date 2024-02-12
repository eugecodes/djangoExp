from auditlog.registry import auditlog
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import StatusModel, TimeStampedModel

from energy_costs.choices import EnergyCostStatus


class EnergyCost(StatusModel, TimeStampedModel, EnergyCostStatus):
    code = models.CharField(max_length=256, unique=True)
    concept = models.CharField(max_length=256, unique=True)
    amount = models.DecimalField(max_digits=14, decimal_places=6)

    class Meta:
        verbose_name = _("EnergyCost")

    def __str__(self):
        return f"{self._meta.verbose_name}: {self.id} - {self.code}"


auditlog.register(EnergyCost)
