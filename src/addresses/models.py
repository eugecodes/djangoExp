from auditlog.registry import auditlog
from django.db import models
from django.db.models import CASCADE
from django.utils.translation import gettext_lazy as _
from model_utils.models import StatusModel, TimeStampedModel

from addresses.choices import AddressStatus


class Address(StatusModel, TimeStampedModel, AddressStatus):
    channel = models.ForeignKey(
        "channels.Channel",
        on_delete=CASCADE,
        null=False,
        blank=False,
        related_name="addresses",
    )

    address = models.CharField(max_length=256)
    postal_code = models.CharField(max_length=10)
    city = models.CharField(max_length=256)
    province = models.CharField(max_length=256)

    class Meta:
        verbose_name = _("Address")

    def __str__(self):
        return f"{self._meta.verbose_name}: {self.id} - {self.address}"


auditlog.register(Address)
