from django.utils.translation import gettext_lazy as _
from model_utils import Choices


class OtherCostStatus:
    ENABLED = "enabled"
    DISABLED = "disabled"
    STATUS = Choices((ENABLED, _("Enabled")), (DISABLED, _("Disabled")))


class OtherCostType:
    EUR_MONTH = "eur/month"
    PERCENTAGE = "percentage"
    EUR_KWH = "eur/kwh"
    OTHER_COSTS = Choices(
        (EUR_MONTH, _("eur/month")),
        (PERCENTAGE, _("percentage")),
        (EUR_KWH, _("eur/kwh")),
    )
