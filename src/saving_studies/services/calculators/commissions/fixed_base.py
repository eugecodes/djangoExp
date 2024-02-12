import logging
from decimal import Decimal

from rates.models import Rate
from saving_studies.services.calculators.commissions.base import CommissionCalculator

logger = logging.getLogger(__name__)


class CommissionCalculatorFixedBase(CommissionCalculator):
    def compute_commission(self, rate: Rate, applied_margin: Decimal) -> Decimal:
        percentage_test_commission = (
            rate.commission.percentage_test_commission
            if rate.commission
            and rate.commission
            and rate.commission.percentage_test_commission
            else Decimal("0")
        )

        logger.info(
            "[saving_study_id=%s] Detailed theoretical_commission for rate %s annual_consumption=%s "
            "applied_margin=%s percentage_test_commission=%s",
            self.saving_study.id,
            rate.name,
            self.saving_study.annual_consumption,
            applied_margin,
            percentage_test_commission,
        )

        return (
            self.saving_study.annual_consumption
            * applied_margin
            * percentage_test_commission
            / 100
        )
