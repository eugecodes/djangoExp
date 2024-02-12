import pytest

from common.choices import EnergyTypes
from rate_types.api.schemas.requests import RateTypeRequest


@pytest.fixture
def rate_type_create_request(channel):
    data = RateTypeRequest(name="TestRateType", energy_type=EnergyTypes.GAS)
    yield data


@pytest.fixture
def rate_type_update_request():
    data = RateTypeRequest(name="NewTestRateType", energy_type=EnergyTypes.GAS)
    yield data
