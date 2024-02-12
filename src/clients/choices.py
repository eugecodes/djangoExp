from django.utils.translation import gettext_lazy as _
from model_utils import Choices


class ClientStatus:
    ENABLED = "enabled"
    DISABLED = "disabled"
    STATUS = Choices((ENABLED, _("Enabled")), (DISABLED, _("Disabled")))


class ClientTypes:
    COMPANY = "company"
    SELF_EMPLOYED = "self-employed"
    PARTICULAR = "particular"
    COMMUNITY_OWNERS = "community-owners"
    CLIENT_TYPES = Choices(
        (COMPANY, _("Company")),
        (SELF_EMPLOYED, _("Self Employed")),
        (PARTICULAR, _("Particular")),
        (COMMUNITY_OWNERS, _("Community Owners")),
    )


class InvoiceNotificationTypes:
    EMAIL = "email"
    POSTAL = "postal"
    INVOICE_NOTIFICATION_TYPES = Choices((EMAIL, _("Email")), (POSTAL, _("Postal")))
