from decimal import Decimal

import pytest

from energy_costs.api.schemas.requests import EnergyCostRequest, EnergyCostUpdateRequest


@pytest.fixture
def energy_cost_create_request():
    data = EnergyCostRequest(
        code="TestEnergyCost", concept="test concept", amount=Decimal(10)
    )
    yield data


@pytest.fixture
def energy_cost_update_request():
    data = EnergyCostUpdateRequest(
        code="NewTestEnergyCost", concept="test concept", amount=Decimal(10)
    )
    yield data
