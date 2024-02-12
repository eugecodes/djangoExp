from django.utils.translation import gettext_lazy as _
from model_utils import Choices


class {{ cookiecutter.app_name }}Status:
    ENABLED = "enabled"
    DISABLED = "disabled"
    STATUS = Choices((ENABLED, _("Enabled")), (DISABLED, _("Disabled")))
