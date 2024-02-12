from django.utils.translation import gettext_lazy as _
from model_utils import Choices


class MarginStatus:
    ENABLED = "enabled"
    DISABLED = "disabled"
    STATUS = Choices((ENABLED, _("Enabled")), (DISABLED, _("Disabled")))


class MarginType:
    RATE_TYPE = "rate_type"
    CONSUME_RANGE = "consume_range"
    MARGIN_TYPES = Choices(
        (RATE_TYPE, _("Rate Type")), (CONSUME_RANGE, _("Consume Range"))
    )
