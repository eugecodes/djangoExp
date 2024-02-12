from decimal import Decimal

import pytest

from clients.choices import ClientTypes
from common.choices import EnergyTypes
from rates.api.schemas.requests import RateRequest, RateUpdateRequest
from rates.choices import PriceTypes


@pytest.fixture
def rate_create_request(channel, rate_type, marketer):
    data = RateRequest(
        name="Rate",
        energy_type=EnergyTypes.ELECTRICITY,
        price_type=PriceTypes.BASE,
        client_types=[ClientTypes.COMPANY],
        # max_power="",
        # min_power="",
        # min_consumption="",
        # max_consumption="",
        # energy_price_1="",
        # energy_price_2="",
        # energy_price_3="",
        # energy_price_4="",
        # energy_price_5="",
        # energy_price_6="",
        # power_price_1="",
        # power_price_2="",
        # power_price_3="",
        # power_price_4="",
        # power_price_5="",
        # power_price_6="",
        fixed_term_price=Decimal(10),
        permanency=True,
        length=12,
        is_full_renewable=True,
        compensation_surplus=False,
        compensation_surplus_value=Decimal(10),
        rate_type_id=rate_type.id,
        marketer_id=marketer.id,
    )
    yield data


@pytest.fixture
def rate_update_request(rate_type):
    data = RateUpdateRequest(
        name="NewTestRate",
        energy_type=EnergyTypes.ELECTRICITY,
        price_type=PriceTypes.BASE,
        client_types=[ClientTypes.COMPANY],
        fixed_term_price=Decimal(10),
        permanency=True,
        length=12,
        is_full_renewable=True,
        compensation_surplus=False,
        compensation_surplus_value=Decimal(10),
        rate_type_id=rate_type.id,
    )
    yield data
