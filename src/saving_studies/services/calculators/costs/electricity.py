import logging
from decimal import Decimal

from moneyed import Money

from energy_costs.constants import ELECTRICITY_TAX
from energy_costs.models import EnergyCost
from rates.choices import PriceTypes
from saving_studies.services.calculators.costs.base import CostCalculator
from saving_studies.services.calculators.costs.schema import CostCalculatorInfo
from suggested_rates.services.schema import SuggestedRateCosts

logger = logging.getLogger(__name__)


class CostCalculatorElectricity(CostCalculator):
    def compute_total_cost(
        self,
        cost_calculator_info: CostCalculatorInfo,
        applied_margin: Money,
        current_other_cost: bool = False,
    ) -> SuggestedRateCosts:
        energy_cost = self.get_energy_cost(cost_calculator_info, applied_margin)
        power_cost = self.get_power_cost(cost_calculator_info)
        other_costs = (
            self.get_current_other_costs(power_cost, energy_cost)
            if current_other_cost
            else self.get_others_costs(power_cost, energy_cost)
        )
        ie_cost = self.get_ie() * (energy_cost + power_cost + other_costs)
        iva_cost = self.get_vat() * (energy_cost + power_cost + other_costs + ie_cost)

        starting_log = (
            f"Detailed cost for rate {cost_calculator_info.name}"
            if current_other_cost
            else "Current cost for saving study with"
        )
        logger.info(
            f"[saving_study_id={self.saving_study.id}] {starting_log} energy_cost={energy_cost} "
            f"power_cost={power_cost} other_costs={other_costs} ie_cost={ie_cost} "
            f"iva_cost={iva_cost}"
        )
        costs = SuggestedRateCosts(
            total_cost=energy_cost + power_cost + other_costs + ie_cost + iva_cost,
            energy_cost=energy_cost,
            power_cost=power_cost,
            other_costs=other_costs,
            ie_cost=ie_cost,
            iva_cost=iva_cost,
        )
        return costs

    def get_energy_cost(
        self, cost_calculator_info: CostCalculatorInfo, applied_margin: Money
    ) -> Money:
        cost_list = []
        for i in range(1, 7):
            energy_price = getattr(cost_calculator_info, f"energy_price_{i}")
            consumption = getattr(self.saving_study, f"consumption_p{i}")
            if energy_price is None or consumption is None:
                break
            energy_price = (
                energy_price + applied_margin
                if cost_calculator_info.price_type == PriceTypes.BASE
                else energy_price
            )
            cost_list.append(energy_price * consumption)
        return sum(cost_list)

    def get_power_cost(self, cost_calculator_info: CostCalculatorInfo) -> Money:
        cost_list = []
        for i in range(1, 7):
            power_price = getattr(cost_calculator_info, f"power_price_{i}")
            power = getattr(self.saving_study, f"power_{i}")
            if power_price is None or power is None:
                break
            cost_list.append(power_price * power)
        return sum(cost_list) * Decimal(self.saving_study.analyzed_days)

    def get_ie(self) -> Decimal:
        ie = EnergyCost.objects.get(code=ELECTRICITY_TAX)
        if not ie:
            return Decimal("0")
        return ie.amount / 100
