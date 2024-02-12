from auditlog.registry import auditlog
from django.db import models
from django.db.models import JSONField
from django.utils.translation import gettext_lazy as _
from djmoney.models.fields import MoneyField
from model_utils.models import StatusModel, TimeStampedModel

from costs.choices import OtherCostStatus, OtherCostType


class OtherCost(StatusModel, TimeStampedModel, OtherCostStatus):
    name = models.CharField(max_length=256, unique=True)
    mandatory = models.BooleanField(null=False, blank=False)
    client_types = JSONField("ClientTypes")
    max_power = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    min_power = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    type = models.CharField(max_length=11, choices=OtherCostType.OTHER_COSTS)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    extra_fee = MoneyField(max_digits=10, decimal_places=2, null=True, blank=True)

    # rates = relationship(
    #     "Rate", secondary=other_cost_rates_association, backref="other_costs"
    # )

    class Meta:
        verbose_name = _("OtherCost")

    def __str__(self):
        return f"{self._meta.verbose_name}: {self.id} - {self.name}"


auditlog.register(OtherCost)
