import pytest

from clients.choices import ClientTypes
from costs.api.schemas.requests import OtherCostRequest, OtherCostUpdateRequest
from costs.choices import OtherCostType


@pytest.fixture
def cost_create_request():
    data = OtherCostRequest(
        name="TestOtherCost",
        mandatory=True,
        type=OtherCostType.PERCENTAGE,
        client_types=[ClientTypes.COMPANY],
        quantity=1,
        max_power=10,
        min_power=1,
    )
    yield data


@pytest.fixture
def cost_update_request():
    data = OtherCostUpdateRequest(
        name="NewTestOtherCost",
        mandatory=True,
        type=OtherCostType.PERCENTAGE,
        client_types=[ClientTypes.COMPANY],
        quantity=1,
        max_power=10,
        min_power=1,
    )
    yield data
