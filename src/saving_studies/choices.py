from django.utils.translation import gettext_lazy as _
from model_utils import Choices


class SavingStudyStatus:
    IN_PROGRESS = "in-progress"
    COMPLETED = "completed"
    DISABLED = "disabled"
    STATUS = Choices(
        (IN_PROGRESS, _("In Progress")),
        (COMPLETED, _("Completed")),
        (DISABLED, _("Disabled")),
    )
