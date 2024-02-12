from django.utils.translation import gettext_lazy as _
from model_utils import Choices


class CommissionStatus:
    ENABLED = "enabled"
    DISABLED = "disabled"
    STATUS = Choices((ENABLED, _("Enabled")), (DISABLED, _("Disabled")))


class RangeType:
    POWER = "power"
    CONSUMPTION = "consumption"
    RANGE_TYPES = Choices((POWER, _("Power")), (CONSUMPTION, _("Consumption")))
