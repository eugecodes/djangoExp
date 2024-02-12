from abc import ABC, abstractmethod
from decimal import Decimal

from rates.models import Rate
from saving_studies.models import SavingStudy


class CommissionCalculator(ABC):
    def __init__(self, saving_study: SavingStudy):
        self.saving_study = saving_study

    @abstractmethod
    def compute_commission(self, rate: Rate, applied_margin: Decimal) -> Decimal:
        raise NotImplementedError
