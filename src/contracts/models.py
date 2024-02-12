from auditlog.registry import auditlog
from django.db import models
from django.db.models import CASCADE
from django.utils.translation import gettext_lazy as _
from model_utils.models import StatusModel, TimeStampedModel
from phonenumber_field.modelfields import PhoneNumberField

from contracts.choices import ContractStatus


class Contract(StatusModel, TimeStampedModel, ContractStatus):
    channel = models.ForeignKey(
        "channels.Channel",
        on_delete=CASCADE,
        null=False,
        blank=False,
        related_name="contracts",
    )

    supply_point = models.ForeignKey(
        "supply_points.SupplyPoint",
        on_delete=CASCADE,
        null=False,
        blank=False,
        related_name="contracts",
    )

    client = models.ForeignKey(
        "clients.Client",
        on_delete=CASCADE,
        null=False,
        blank=False,
        related_name="contracts",
    )

    rate = models.ForeignKey(
        "rates.Rate",
        on_delete=CASCADE,
        null=False,
        blank=False,
        related_name="contracts",
    )

    saving_study = models.ForeignKey(
        "saving_studies.SavingStudy",
        on_delete=CASCADE,
        null=True,
        blank=True,
        related_name="contracts",
    )

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

    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    expected_end_date = models.DateField(null=True, blank=True)
    preferred_start_date = models.DateField(null=True, blank=True)
    period = models.IntegerField(null=True, blank=True)

    signature_first_name = models.CharField(max_length=128)
    signature_last_name = models.CharField(max_length=128)
    signature_dni = models.CharField(max_length=20, null=True, blank=True)
    signature_email = models.CharField(max_length=256, null=True, blank=True)
    signature_phone = PhoneNumberField(null=True, blank=True)

    class Meta:
        verbose_name = _("Contract")

    def __str__(self):
        return f"{self._meta.verbose_name}: {self.id}"


auditlog.register(Contract)
