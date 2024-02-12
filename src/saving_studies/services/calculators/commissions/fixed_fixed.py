import logging
from decimal import Decimal

from commissions.choices import RangeType
from rates.models import Rate
from saving_studies.services.calculators.commissions.base import CommissionCalculator

logger = logging.getLogger(__name__)


class CommissionCalculatorFixedFixed(CommissionCalculator):
    def compute_commission(
        self, rate: Rate, applied_margin: Decimal | None = None
    ) -> Decimal:
        theoretical_commission = Decimal("0")
        power = self.saving_study.power_6 or self.saving_study.power_2
        # for commission in rate.commissions:
        commission = rate.commission
        if (
            commission.rate_type_segmentation
            and (
                commission.range_type == RangeType.CONSUMPTION
                and (
                    commission.min_consumption
                    <= self.saving_study.annual_consumption
                    <= commission.max_consumption
                )
            )
            or (
                commission.range_type == RangeType.POWER
                and (commission.min_power <= power <= commission.max_power)
            )
        ):
            theoretical_commission += commission.test_commission

        logger.info(
            f"[saving_study_id={self.saving_study.id}] Detailed theoretical_commission for rate {rate.name} theoretical_commission={theoretical_commission}"
        )

        return theoretical_commission
