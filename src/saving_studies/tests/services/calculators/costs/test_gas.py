from decimal import Decimal

import pytest
from moneyed import Money

from config import settings
from energy_costs.constants import VAT, OIL_TAX
from energy_costs.models import EnergyCost
from saving_studies.services.calculators.costs.gas import CostCalculatorGas
from saving_studies.services.calculators.costs.schema import CostCalculatorInfo


@pytest.mark.django_db
def test_init(saving_study):
    calculator = CostCalculatorGas(saving_study)
    assert calculator.saving_study == saving_study


@pytest.mark.django_db
def test_get_vat(saving_study):
    calculator = CostCalculatorGas(saving_study)
    vat = EnergyCost.objects.get(code=VAT)
    assert calculator.get_vat() == vat.amount / 100


@pytest.mark.django_db
def test_get_ih(saving_study):
    calculator = CostCalculatorGas(saving_study)
    ih = EnergyCost.objects.get(code=OIL_TAX)
    assert calculator.get_ih() == ih.amount


@pytest.mark.django_db
def test_get_energy_cost(saving_study):
    money_margin = Money(10, currency=settings.DEFAULT_CURRENCY)

    saving_study.consumption_p1 = Decimal(1)

    cost_calculator_info = CostCalculatorInfo()
    cost_calculator_info.energy_price_1 = Money(10, currency=settings.DEFAULT_CURRENCY)
    calculator = CostCalculatorGas(saving_study)
    assert calculator.get_energy_cost(cost_calculator_info, money_margin) == Money(
        10, currency=settings.DEFAULT_CURRENCY
    )


@pytest.mark.django_db
def test_get_fixed_cost(saving_study):
    fixed_term_price = Money(10, currency=settings.DEFAULT_CURRENCY)

    saving_study.analyzed_days = 1
    calculator = CostCalculatorGas(saving_study)
    assert calculator.get_fixed_cost(fixed_term_price) == Money(
        10, currency=settings.DEFAULT_CURRENCY
    )


@pytest.mark.django_db
def test_compute_total_cost(saving_study):
    money_margin = Money(10, currency=settings.DEFAULT_CURRENCY)

    saving_study.analyzed_days = 1
    saving_study.consumption_p1 = Decimal(1)

    cost_calculator_info = CostCalculatorInfo()
    cost_calculator_info.fixed_term_price = Money(
        10, currency=settings.DEFAULT_CURRENCY
    )
    cost_calculator_info.energy_price_1 = Money(10, currency=settings.DEFAULT_CURRENCY)
    calculator = CostCalculatorGas(saving_study)
    cost = calculator.compute_total_cost(cost_calculator_info, money_margin)

    expected_energy_cost = Money(10, currency=settings.DEFAULT_CURRENCY)
    expected_fixed_cost = Money(10, currency=settings.DEFAULT_CURRENCY)
    expected_other_costs = Money(0, currency=settings.DEFAULT_CURRENCY)
    ih_tax = EnergyCost.objects.get(code=OIL_TAX)
    expected_ih_cost = Money(
        ih_tax.amount * saving_study.consumption_p1, currency=settings.DEFAULT_CURRENCY
    )

    vat_tax = EnergyCost.objects.get(code=VAT)
    expected_vat_cost = (
        vat_tax.amount
        * (
            expected_ih_cost
            + expected_energy_cost
            + expected_fixed_cost
            + expected_other_costs
        )
        / 100
    )

    expected_total_cost = (
        expected_vat_cost
        + expected_ih_cost
        + expected_energy_cost
        + expected_fixed_cost
        + expected_other_costs
    )

    assert cost.total_cost == expected_total_cost
    assert cost.energy_cost == expected_energy_cost
    assert cost.fixed_cost == expected_fixed_cost
    assert cost.other_costs == expected_other_costs
    assert cost.ih_cost == expected_ih_cost
    assert cost.iva_cost == expected_vat_cost
