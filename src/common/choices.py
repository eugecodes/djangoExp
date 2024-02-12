from django.utils.translation import gettext_lazy as _
from model_utils import Choices


class EnergyTypes:
    ELECTRICITY = "electricity"
    GAS = "gas"
    ENERGY_TYPES = Choices((ELECTRICITY, _("Electricity")), (GAS, _("Gas")))
