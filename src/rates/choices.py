from django.utils.translation import gettext_lazy as _
from model_utils import Choices


class RateStatus:
    ENABLED = "enabled"
    DISABLED = "disabled"
    STATUS = Choices((ENABLED, _("Enabled")), (DISABLED, _("Disabled")))


class PriceTypes:
    FIXED = "fixed_fixed"
    BASE = "fixed_base"
    INDEXED = "indexed"
    PRICE_TYPES = Choices(
        (FIXED, _("Fixed")), (BASE, _("Base")), (INDEXED, _("Indexed"))
    )
