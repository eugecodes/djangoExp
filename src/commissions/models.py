from auditlog.registry import auditlog
from django.db import models
from django.db.models import CASCADE
from django.utils.translation import gettext_lazy as _
from model_utils.models import StatusModel, TimeStampedModel

from commissions.choices import CommissionStatus, RangeType


class Commission(StatusModel, TimeStampedModel, CommissionStatus):
    name = models.CharField(max_length=124)
    percentage_test_commission = models.IntegerField(null=True, blank=True)
    range_type = models.CharField(
        max_length=11, choices=RangeType.RANGE_TYPES, null=True, blank=True
    )

    rate_type_segmentation = models.BooleanField(null=True, blank=True)

    min_consumption = models.DecimalField(
        max_digits=14, decimal_places=2, null=True, blank=True
    )
    max_consumption = models.DecimalField(
        max_digits=14, decimal_places=2, null=True, blank=True
    )
    min_power = models.DecimalField(
        max_digits=14, decimal_places=2, null=True, blank=True
    )
    max_power = models.DecimalField(
        max_digits=14, decimal_places=2, null=True, blank=True
    )
    test_commission = models.DecimalField(
        max_digits=14, decimal_places=2, null=True, blank=True
    )

    rate_type = models.ForeignKey(
        "rate_types.RateType", on_delete=CASCADE, related_name="commissions"
    )

    class Meta:
        verbose_name = _("Commission")

    def __str__(self):
        return f"{self._meta.verbose_name}: {self.id} - {self.name}"


auditlog.register(Commission)
