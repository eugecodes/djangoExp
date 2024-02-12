from django.utils.translation import gettext_lazy as _
from model_utils import Choices


class ContractStatus:
    INCOMPLETE = "incomplete"
    REQUESTED = "requested"
    WAITING_MARKETER = "waiting-marketer"
    WAITING_CLIENT_SIGN = "waiting-client-sign"
    SIGNED = "signed"
    ACTIVATED = "activated"
    FINISHED = "finished"
    MARKETER_ISSUE = "marketer-issue"
    DISTRIBUTOR_ISSUE = "distributor-issue"
    CANCELLED = "cancelled"

    STATUS = Choices(
        (INCOMPLETE, _("Incomplete")),
        (REQUESTED, _("Requested")),
        (WAITING_MARKETER, _("Waiting Marketer")),
        (WAITING_CLIENT_SIGN, _("Waiting Client Sign")),
        (SIGNED, _("Signed")),
        (ACTIVATED, _("Activated")),
        (FINISHED, _("Finished")),
        (MARKETER_ISSUE, _("Marketer Issue")),
        (DISTRIBUTOR_ISSUE, _("Distributor Issue")),
        (CANCELLED, _("Cancelled")),
    )
