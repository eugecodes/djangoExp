from auditlog.registry import auditlog
from django.db import models
from django.db.models import CASCADE
from django.utils.translation import gettext_lazy as _
from model_utils.models import StatusModel, TimeStampedModel
from phonenumber_field.modelfields import PhoneNumberField

from contacts.choices import ContactStatus


class Contact(StatusModel, TimeStampedModel, ContactStatus):
    name = models.CharField(max_length=256)
    email = models.EmailField(null=True, blank=True)
    phone = PhoneNumberField(null=True, blank=True)

    client = models.ForeignKey(
        "clients.Client", on_delete=CASCADE, related_name="contacts"
    )
    is_main_contact = models.BooleanField(default=False, null=False, blank=False)

    class Meta:
        verbose_name = _("Contact")

    def __str__(self):
        return f"{self._meta.verbose_name}: {self.id} - {self.name}"


auditlog.register(Contact)
