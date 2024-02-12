from decimal import Decimal

import pytest
from moneyed import Money

from config import settings
from energy_costs.constants import VAT, ELECTRICITY_TAX
from energy_costs.models import EnergyCost
from saving_studies.services.calculators.costs.electricity import (
    CostCalculatorElectricity,
)
from saving_studies.services.calculators.costs.schema import CostCalculatorInfo


@pytest.mark.django_db
def test_init(saving_study):
    calculator = CostCalculatorElectricity(saving_study)
    assert calculator.saving_study == saving_study


@pytest.mark.django_db
def test_get_vat(saving_study):
    calculator = CostCalculatorElectricity(saving_study)
    vat = EnergyCost.objects.get(code=VAT)
    assert calculator.get_vat() == vat.amount / 100


@pytest.mark.django_db
def test_get_ie(saving_study):
    calculator = CostCalculatorElectricity(saving_study)
    ie = EnergyCost.objects.get(code=ELECTRICITY_TAX)
    assert calculator.get_ie() == ie.amount / 100


@pytest.mark.django_db
def test_get_power_cost(saving_study):
    saving_study.analyzed_days = 1
    saving_study.power_1 = Decimal(1)

    cost_calculator_info = CostCalculatorInfo()
    cost_calculator_info.power_price_1 = Money(10, currency=settings.DEFAULT_CURRENCY)
    calculator = CostCalculatorElectricity(saving_study)
    assert calculator.get_power_cost(cost_calculator_info) == Money(
        10, currency=settings.DEFAULT_CURRENCY
    )


@pytest.mark.django_db
def test_get_power_cost_multiple_days(saving_study):
    saving_study.analyzed_days = 100
    saving_study.power_1 = Decimal(10)

    cost_calculator_info = CostCalculatorInfo()
    cost_calculator_info.power_price_1 = Money(10, currency=settings.DEFAULT_CURRENCY)
    calculator = CostCalculatorElectricity(saving_study)
    assert calculator.get_power_cost(cost_calculator_info) == Money(
        10000, currency=settings.DEFAULT_CURRENCY
    )


@pytest.mark.django_db
def test_get_power_cost_multiple_power(saving_study):
    saving_study.analyzed_days = 1
    saving_study.power_1 = Decimal(1)
    saving_study.power_2 = Decimal(1)

    cost_calculator_info = CostCalculatorInfo()
    cost_calculator_info.power_price_1 = Money(10, currency=settings.DEFAULT_CURRENCY)
    cost_calculator_info.power_price_2 = Money(10, currency=settings.DEFAULT_CURRENCY)
    calculator = CostCalculatorElectricity(saving_study)
    assert calculator.get_power_cost(cost_calculator_info) == Money(
        20, currency=settings.DEFAULT_CURRENCY
    )


@pytest.mark.django_db
def test_get_energy_cost(saving_study):
    money_margin = Money(10, currency=settings.DEFAULT_CURRENCY)

    saving_study.consumption_p1 = Decimal(1)

    cost_calculator_info = CostCalculatorInfo()
    cost_calculator_info.energy_price_1 = Money(10, currency=settings.DEFAULT_CURRENCY)
    calculator = CostCalculatorElectricity(saving_study)
    assert calculator.get_energy_cost(cost_calculator_info, money_margin) == Money(
        10, currency=settings.DEFAULT_CURRENCY
    )


@pytest.mark.django_db
def test_get_energy_cost_multiple_consumption(saving_study):
    money_margin = Money(10, currency=settings.DEFAULT_CURRENCY)

    saving_study.consumption_p1 = Decimal(1)
    saving_study.consumption_p2 = Decimal(1)

    cost_calculator_info = CostCalculatorInfo()
    cost_calculator_info.energy_price_1 = Money(10, currency=settings.DEFAULT_CURRENCY)
    cost_calculator_info.energy_price_2 = Money(10, currency=settings.DEFAULT_CURRENCY)
    calculator = CostCalculatorElectricity(saving_study)
    assert calculator.get_energy_cost(cost_calculator_info, money_margin) == Money(
        20, currency=settings.DEFAULT_CURRENCY
    )


@pytest.mark.django_db
def test_compute_total_cost(saving_study):
    money_margin = Money(10, currency=settings.DEFAULT_CURRENCY)

    saving_study.analyzed_days = 1
    saving_study.power_1 = Decimal(1)

    saving_study.consumption_p1 = Decimal(1)

    cost_calculator_info = CostCalculatorInfo()
    cost_calculator_info.energy_price_1 = Money(10, currency=settings.DEFAULT_CURRENCY)
    cost_calculator_info.power_price_1 = Money(10, currency=settings.DEFAULT_CURRENCY)
    calculator = CostCalculatorElectricity(saving_study)
    cost = calculator.compute_total_cost(cost_calculator_info, money_margin)

    expected_energy_cost = Money(10, currency=settings.DEFAULT_CURRENCY)
    expected_power_cost = Money(10, currency=settings.DEFAULT_CURRENCY)
    expected_other_costs = Money(0, currency=settings.DEFAULT_CURRENCY)
    ie_tax = EnergyCost.objects.get(code=ELECTRICITY_TAX)
    expected_ie_cost = (
        ie_tax.amount
        * (expected_energy_cost + expected_power_cost + expected_other_costs)
        / 100
    )
    vat_tax = EnergyCost.objects.get(code=VAT)
    expected_vat_cost = (
        vat_tax.amount
        * (
            expected_ie_cost
            + expected_energy_cost
            + expected_power_cost
            + expected_other_costs
        )
        / 100
    )

    expected_total_cost = (
        expected_vat_cost
        + expected_ie_cost
        + expected_energy_cost
        + expected_power_cost
        + expected_other_costs
    )

    assert cost.total_cost == expected_total_cost
    assert cost.energy_cost == expected_energy_cost
    assert cost.power_cost == expected_power_cost
    assert cost.other_costs == expected_other_costs
    assert cost.ie_cost == expected_ie_cost
    assert cost.iva_cost == expected_vat_cost
