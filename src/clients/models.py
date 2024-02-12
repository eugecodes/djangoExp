from auditlog.registry import auditlog
from django.db import models
from django.db.models import CASCADE
from django.utils.translation import gettext_lazy as _
from model_utils.models import StatusModel, TimeStampedModel

from clients.choices import ClientStatus, ClientTypes, InvoiceNotificationTypes
from common.mixins import BankDataMixin


class Client(
    StatusModel,
    TimeStampedModel,
    ClientStatus,
    BankDataMixin
    # RulesModelMixin,
    # metaclass=RulesModelBase,
):
    channel = models.ForeignKey(
        "channels.Channel",
        on_delete=CASCADE,
        null=False,
        blank=False,
        related_name="clients",
    )
    fiscal_name = models.CharField(max_length=256)
    cif = models.CharField(max_length=10, unique=True)

    alias = models.CharField(max_length=64)

    client_type = models.CharField(max_length=20, choices=ClientTypes.CLIENT_TYPES)
    invoice_notification_type = models.CharField(
        max_length=20, choices=InvoiceNotificationTypes.INVOICE_NOTIFICATION_TYPES
    )

    invoice_email = models.EmailField(null=True, blank=True)
    invoice_postal = models.CharField(max_length=64, null=True, blank=True)

    is_renewable = models.BooleanField(default=False)

    # contacts = relationship(Contact, back_populates="client", uselist=True)
    # user = relationship("User", back_populates="clients")
    # supply_points = relationship("SupplyPoint", back_populates="client")

    class Meta:
        verbose_name = _("Client")
        unique_together = (("channel", "cif"), ("channel", "alias"))
        permissions = (("assign_task", "Assign task"),)

    def __str__(self):
        return f"{self._meta.verbose_name}: {self.id} - {self.fiscal_name}"


auditlog.register(Client)
