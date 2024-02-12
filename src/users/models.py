from auditlog.registry import auditlog
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CASCADE
from django.utils.translation import gettext_lazy as _
from model_utils.models import StatusModel, TimeStampedModel

from users.choices import UserStatus
from users.managers import CustomUserManager


class Token(TimeStampedModel):
    token = models.CharField(max_length=128, unique=True, null=False, blank=False)
    user = models.ForeignKey(
        "users.User", on_delete=CASCADE, null=False, blank=False, related_name="tokens"
    )

    def __str__(self):
        return f"{self.Meta.__name__} - {self.token}"


class User(AbstractUser, StatusModel, TimeStampedModel, UserStatus):
    username = None
    email = models.EmailField(unique=True)

    channel = models.ForeignKey(
        "channels.Channel", on_delete=CASCADE, null=True, blank=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("User")

    def __str__(self):
        return f"{self._meta.verbose_name}: {self.id} - {self.email}"


auditlog.register(User)
