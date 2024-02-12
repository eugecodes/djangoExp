import logging
from decimal import Decimal
from typing import List

from django.db.models import QuerySet

from margins.choices import MarginType
from margins.models import Margin
from rates.models import Rate
from saving_studies.models import SavingStudy
from saving_studies.services.calculators.factory import CalculatorsFactory
from suggested_rates.models import SuggestedRate
from suggested_rates.services.schema import SuggestedRateCosts

logger = logging.getLogger(__name__)


class SuggestedRatesGenerator:
    def __init__(self, saving_study: SavingStudy) -> None:
        self.saving_study = saving_study

    def get_default_margin_rate(self, rate: Rate) -> Margin:
        if (
            rate.margin.count() == 1
            and rate.margin.first().type == MarginType.RATE_TYPE
        ):
            return rate.margin.first()

        if not self.saving_study.annual_consumption:
            return self.get_margin_with_min_consumption(rate.margin)

        # filter only the margin inside the consume range
        margins_in_range = rate.margin.filter(
            min_consumption__lte=self.saving_study.annual_consumption,
            max_consumption__gte=self.saving_study.annual_consumption,
        )

        return margins_in_range.first() if margins_in_range.count() == 1 else None

    def get_margin_with_min_consumption(self, margins: QuerySet) -> Margin | None:
        margins_with_min_consumption = margins.filter(min_consumption__isnull=False)
        if margins_with_min_consumption.exists():
            return min(
                margins_with_min_consumption, key=lambda margin: margin.min_consumption
            )

    def generate_suggested_rates(self, rates: QuerySet) -> List[SuggestedRate]:
        logger.info(
            f"[saving_study_id={self.saving_study.id}] Generating suggested rates..."
        )
        # clean previous suggested rates
        SuggestedRate.objects.filter(
            id__in=self.saving_study.suggested_rates.values_list("id", flat=True)
        ).delete()
        current_cost = Decimal("0")
        if self.saving_study.is_compare_conditions:
            current_cost = self.compute_current_cost()
        for rate in rates:
            default_margin = self.get_default_margin_rate(rate)
            applied_margin = (
                default_margin.min_margin if default_margin else Decimal("0")
            )
            costs, theoretical_commission = self.compute_final_cost_and_commission(
                rate, applied_margin
            )
            other_costs_commission = self.compute_other_costs_commission(rate)

            suggested_rate = SuggestedRate(
                saving_study_id=self.saving_study.id,
                marketer_name=rate.marketer.name,
                has_contractual_commitment=rate.permanency,
                duration=rate.length,
                rate_name=rate.name,
                is_full_renewable=getattr(rate, "is_full_renewable", False) or False,
                has_net_metering=getattr(rate, "compensation_surplus", False) or False,
                net_metering_value=getattr(rate, "compensation_surplus_value", 0) or 0,
                profit_margin_type=getattr(default_margin, "type", None),
                max_profit_margin=getattr(default_margin, "max_margin", 0) or 0,
                min_profit_margin=getattr(default_margin, "min_margin", 0) or 0,
                applied_profit_margin=applied_margin,
                energy_price_1=rate.energy_price_1,
                energy_price_2=rate.energy_price_2,
                energy_price_3=rate.energy_price_3,
                energy_price_4=rate.energy_price_4,
                energy_price_5=rate.energy_price_5,
                energy_price_6=rate.energy_price_6,
                power_price_1=rate.power_price_1,
                power_price_2=rate.power_price_2,
                power_price_3=rate.power_price_3,
                power_price_4=rate.power_price_4,
                power_price_5=rate.power_price_5,
                power_price_6=rate.power_price_6,
                fixed_term_price=rate.fixed_term_price,
                price_type=rate.price_type,
                final_cost=costs.final_cost,
                energy_cost=costs.energy_cost,
                other_costs=costs.other_costs,
                iva_cost=costs.iva_cost,
                power_cost=costs.power_cost,
                ie_cost=costs.ie_cost,
                fixed_cost=costs.fixed_cost,
                ih_cost=costs.ih_cost,
                total_commission=theoretical_commission + other_costs_commission,
                theoretical_commission=theoretical_commission,
                other_costs_commission=other_costs_commission,
            )

            if self.saving_study.is_compare_conditions and current_cost:
                suggested_rate.saving_relative = (
                    (current_cost - costs.final_cost) / current_cost * 100
                )
                suggested_rate.saving_absolute = current_cost - costs.final_cost

            logger.info(
                f"[saving_study_id={self.saving_study.id}] Suggested rate generated: applied_margin={applied_margin}"
                f", final_cost={costs.final_cost} rate={suggested_rate}",
            )

        logger.info(
            f"[saving_study_id={self.saving_study.id}] {self.saving_study.suggested_rates.count()} Suggested rates generated",
        )

        return self.saving_study.suggested_rates.all()

    def compute_current_cost(self) -> Decimal:
        logger.info(
            f"[saving_study_id={self.saving_study.id}] Computing current cost with energy {self.saving_study.energy_type}"
        )

        cost_calculator = CalculatorsFactory.init_cost_calculator(self.saving_study)
        # cost_calculator_info = CostCalculatorInfo.from_orm(self.saving_study)
        # cost_calculator_info.fixed_term_price = self.saving_study.fixed_price
        current_cost = cost_calculator.compute_total_cost(
            # cost_calculator_info,
            Decimal("0"),
            current_other_cost=True,
        )

        return current_cost.total_cost

    def compute_final_cost_and_commission(
        self, rate: Rate, applied_margin: Decimal
    ) -> (SuggestedRateCosts, Decimal):
        logger.info(
            f"[saving_study_id={self.saving_study.id}] Computing final cost for rate {rate} with energy  {rate.rate_type.energy_type}"
        )
        commission_calculator = CalculatorsFactory.init_commission_calculator(
            rate.price_type, self.saving_study
        )
        theoretical_commission = commission_calculator.compute_commission(
            rate, applied_margin
        )
        cost_calculator = CalculatorsFactory.init_cost_calculator(
            rate.rate_type.energy_type, self.saving_study
        )
        costs = cost_calculator.compute_total_cost(
            CostCalculatorInfo.from_orm(rate), applied_margin
        )
        costs.final_cost = costs.total_cost + theoretical_commission

        return costs, theoretical_commission

    def compute_other_costs_commission(self, rate: Rate) -> Decimal:
        if not rate.other_costs:
            return Decimal("0")
        return sum(cost.extra_fee for cost in rate.other_costs)
