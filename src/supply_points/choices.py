from django.utils.translation import gettext_lazy as _
from model_utils import Choices


class SupplyPointStatus:
    ENABLED = "enabled"
    DISABLED = "disabled"
    STATUS = Choices((ENABLED, _("Enabled")), (DISABLED, _("Disabled")))


class CounterType:
    NORMAL = "normal"
    TELEMATIC = "telematic"
    TYPES = Choices((NORMAL, _("Normal")), (TELEMATIC, _("Telematic")))


class OwnerType:
    SELF = "self"
    MARKETER = "marketer"
    OTHER = "other"
    TYPES = Choices((SELF, _("Self")), (MARKETER, _("Marketer")), (OTHER, _("Other")))
