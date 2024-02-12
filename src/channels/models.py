from auditlog.registry import auditlog
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import StatusModel, TimeStampedModel

from channels.choices import ChannelStatus
from common.mixins import BankDataMixin


class Channel(StatusModel, TimeStampedModel, ChannelStatus, BankDataMixin):
    name = models.CharField(max_length=256, unique=True)
    social_name = models.CharField(max_length=256)
    cif = models.CharField(max_length=256)

    class Meta:
        verbose_name = _("Channel")

    def __str__(self):
        return f"{self._meta.verbose_name}: {self.id} - {self.name}"


auditlog.register(Channel)
