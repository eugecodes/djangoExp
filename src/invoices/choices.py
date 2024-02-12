from django.utils.translation import gettext_lazy as _
from model_utils import Choices


class InvoiceStatus:
    PENDING = "pending"
    PAYED = "payed"
    CANCELED = "canceled"
    STATUS = Choices(
        (PENDING, _("Pending payment")), (PAYED, _("Payed")), (CANCELED, _("Canceled"))
    )
