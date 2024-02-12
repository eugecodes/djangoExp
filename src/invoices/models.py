from auditlog.registry import auditlog
from django.db import models
from django.db.models import CASCADE
from django.utils.translation import gettext_lazy as _
from djmoney.models.fields import MoneyField
from model_utils.models import StatusModel, TimeStampedModel

from invoices.choices import InvoiceStatus


class Invoice(StatusModel, TimeStampedModel, InvoiceStatus):
    channel = models.ForeignKey(
        "channels.Channel",
        on_delete=CASCADE,
        null=False,
        blank=False,
        related_name="invoices",
    )

    invoice_date = models.DateField()
    cif = models.CharField(max_length=10)

    base_price = MoneyField(max_digits=10, decimal_places=2)
    vat = MoneyField(max_digits=10, decimal_places=2)
    total = MoneyField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = _("Invoice")

    def __str__(self):
        return f"{self._meta.verbose_name}: {self.id} - {self.cif}"


auditlog.register(Invoice)
