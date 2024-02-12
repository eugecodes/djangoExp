from auditlog.registry import auditlog
from django.db import models
from django.db.models import CASCADE
from django.utils.translation import gettext_lazy as _
from model_utils.models import StatusModel, TimeStampedModel

from roles.choices import RoleStatus


class Role(StatusModel, TimeStampedModel, RoleStatus):
    name = models.CharField(max_length=256)
    admin_role = models.BooleanField(default=False)

    channel = models.ForeignKey(
        "channels.Channel",
        on_delete=CASCADE,
        null=True,
        blank=True,
        related_name="roles",
    )
    group = models.ForeignKey(
        "auth.Group",
        on_delete=CASCADE,
        null=False,
        blank=False,
        related_name="roles",
    )

    class Meta:
        verbose_name = _("Role")
        unique_together = (("name", "channel"), ("channel", "admin_role"))

    def __str__(self):
        return f"{self._meta.verbose_name}: {self.id} - {self.name}"


auditlog.register(Role)
