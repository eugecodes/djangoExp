from abc import abstractmethod, ABC
from decimal import Decimal

from moneyed import Money

from config import settings
from costs.choices import OtherCostType
from energy_costs.constants import VAT
from energy_costs.models import EnergyCost
from saving_studies.models import SavingStudy
from saving_studies.services.calculators.costs.schema import CostCalculatorInfo
from suggested_rates.services.schema import SuggestedRateCosts

DAYS_PER_MONTH = Decimal("30.4167")
OTHER_COST_FIELDS = {
    "eur/month": "other_cost_kwh",
    "percentage": "other_cost_percentage",
    "eur/kwh": "other_cost_eur_month",
}


class CostCalculator(ABC):
    def __init__(self, saving_study: SavingStudy):
        self.saving_study = saving_study

    @abstractmethod
    def compute_total_cost(
        self,
        cost_calculator_info: CostCalculatorInfo,
        applied_margin: Money,
        current_other_cost: bool = False,
    ) -> SuggestedRateCosts:
        raise NotImplementedError

    @abstractmethod
    def get_energy_cost(
        self, cost_calculator_info: CostCalculatorInfo, applied_margin: Money
    ) -> Money:
        raise NotImplementedError

    def compute_other_cost(
        self,
        type: OtherCostType,
        quantity: Decimal,
        power_cost: Money,
        energy_cost: Money,
    ) -> Decimal:
        if quantity is None:
            return Decimal("0")
        if type == OtherCostType.EUR_MONTH:
            return (
                Decimal(str(self.saving_study.analyzed_days))
                / Decimal(str(DAYS_PER_MONTH))
                * Decimal(str(quantity))
            )
        elif type == OtherCostType.EUR_KWH:
            return Decimal(str(self.saving_study.total_consumption)) * Decimal(
                str(quantity)
            )
        elif type == OtherCostType.PERCENTAGE:
            return Decimal(str((energy_cost + power_cost))) * Decimal(str(quantity))

    def get_others_costs(
        self,
        power_cost: Money,
        energy_cost: Money,
    ) -> Money:
        total_cost = Money(0, currency=settings.DEFAULT_CURRENCY)
        # for other_cost in get_other_costs_rate_study(self.saving_study):
        #     total_cost += self.compute_other_cost(
        #         other_cost.type, other_cost.quantity, power_cost, energy_cost
        #     )
        return total_cost

    @staticmethod
    def get_vat() -> Decimal:
        vat = EnergyCost.objects.get(code=VAT)
        if not vat:
            return Decimal("0")
        return vat.amount / 100

    def get_current_other_costs(self, cost: Money, energy_cost: Money) -> Money:
        return Money(0, currency="EUR")
        return sum(
            [
                self.compute_other_cost(
                    other_cost_type.value,
                    getattr(
                        self.saving_study, OTHER_COST_FIELDS[other_cost_type.value]
                    ),
                    cost,
                    energy_cost,
                )
                for other_cost_type in OtherCostType
            ]
        )
