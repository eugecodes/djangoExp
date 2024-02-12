from common.choices import EnergyTypes
from rates.choices import PriceTypes
from saving_studies.models import SavingStudy
from saving_studies.services.calculators.commissions.base import CommissionCalculator
from saving_studies.services.calculators.commissions.fixed_base import (
    CommissionCalculatorFixedBase,
)
from saving_studies.services.calculators.commissions.fixed_fixed import (
    CommissionCalculatorFixedFixed,
)
from saving_studies.services.calculators.costs.base import CostCalculator
from saving_studies.services.calculators.costs.electricity import (
    CostCalculatorElectricity,
)
from saving_studies.services.calculators.costs.gas import CostCalculatorGas


class CalculatorsFactory:
    COST_CALCULATORS = {
        EnergyTypes.ELECTRICITY: CostCalculatorElectricity,
        EnergyTypes.GAS: CostCalculatorGas,
    }

    COMMISSION_CALCULATORS = {
        PriceTypes.BASE: CommissionCalculatorFixedBase,
        PriceTypes.FIXED: CommissionCalculatorFixedFixed,
    }

    @classmethod
    def init_cost_calculator(cls, saving_study: SavingStudy) -> CostCalculator:
        return cls.COST_CALCULATORS[saving_study.energy_type](saving_study)

    @classmethod
    def init_commission_calculator(
        cls, price_type: str, saving_study: SavingStudy
    ) -> CommissionCalculator:
        return cls.COMMISSION_CALCULATORS[price_type](saving_study)
