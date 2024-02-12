import logging
from decimal import Decimal

from moneyed import Money

from config import settings
from energy_costs.constants import OIL_TAX
from energy_costs.models import EnergyCost
from rates.choices import PriceTypes
from saving_studies.services.calculators.costs.base import CostCalculator
from saving_studies.services.calculators.costs.schema import CostCalculatorInfo
from suggested_rates.services.schema import SuggestedRateCosts

logger = logging.getLogger(__name__)


class CostCalculatorGas(CostCalculator):
    def compute_total_cost(
        self,
        cost_calculator_info: CostCalculatorInfo,
        applied_margin: Money,
        current_other_cost: bool = False,
    ) -> SuggestedRateCosts:
        energy_cost = self.get_energy_cost(cost_calculator_info, applied_margin)
        fixed_cost = self.get_fixed_cost(cost_calculator_info.fixed_term_price)
        other_costs = (
            self.get_current_other_costs(fixed_cost, energy_cost)
            if current_other_cost
            else self.get_others_costs(fixed_cost, energy_cost)
        )
        ih_cost = (
            Money(
                self.get_ih() * self.saving_study.consumption_p1,
                currency=settings.DEFAULT_CURRENCY,
            )
            if self.saving_study.consumption_p1
            else Money(0, currency=settings.DEFAULT_CURRENCY)
        )
        iva_cost = self.get_vat() * (energy_cost + fixed_cost + other_costs + ih_cost)

        starting_log = (
            f"Detailed cost for rate {cost_calculator_info.name}"
            if current_other_cost
            else "Current cost for saving study with"
        )
        logger.info(
            f"[saving_study_id={self.saving_study.id}] {starting_log} energy_cost={energy_cost} "
            f"fixed_cost={fixed_cost} other_costs={other_costs} "
            f"ih_cost={ih_cost} iva_cost={iva_cost}"
        )
        costs = SuggestedRateCosts(
            total_cost=energy_cost + fixed_cost + other_costs + ih_cost + iva_cost,
            energy_cost=energy_cost,
            fixed_cost=fixed_cost,
            other_costs=other_costs,
            ih_cost=ih_cost,
            iva_cost=iva_cost,
        )
        return costs

    def get_energy_cost(
        self, cost_calculator_info: CostCalculatorInfo, applied_margin: Money
    ) -> Money:
        # USE p1 to compute energy cost
        applied_margin = (
            applied_margin
            if cost_calculator_info.price_type == PriceTypes.BASE
            else Money(0, currency=settings.DEFAULT_CURRENCY)
        )
        return (
            cost_calculator_info.energy_price_1 + applied_margin
        ) * self.saving_study.consumption_p1

    def get_fixed_cost(self, fixed_term_price: Money) -> Money:
        return fixed_term_price * self.saving_study.analyzed_days

    def get_ih(self) -> Decimal:
        ih = EnergyCost.objects.get(code=OIL_TAX)
        if not ih:
            return Decimal("0")
        return Decimal(str(ih.amount))
