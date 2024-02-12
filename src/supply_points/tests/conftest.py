from decimal import Decimal

import pytest

from common.choices import EnergyTypes
from config import settings
from supply_points.api.schemas.requests import (
    SupplyPointRequest,
    SupplyPointUpdateRequest,
)
from supply_points.choices import CounterType, OwnerType


@pytest.fixture
def supply_point_create_request(channel, channel_client, address):
    data = SupplyPointRequest(
        channel_id=channel.id,
        client_id=channel_client.id,
        address_id=address.id,
        energy_type=EnergyTypes.ELECTRICITY,
        cups="123",
        counter_type=CounterType.NORMAL,
        counter_property=OwnerType.SELF,
        counter_price_amount=Decimal(1),
        counter_price_currency=settings.DEFAULT_CURRENCY,
    )
    yield data


@pytest.fixture
def supply_point_update_request(address):
    data = SupplyPointUpdateRequest(
        address_id=address.id,
        energy_type=EnergyTypes.ELECTRICITY,
        cups="123",
        counter_type=CounterType.NORMAL,
        counter_property=OwnerType.SELF,
        counter_price_amount=Decimal(1),
        counter_price_currency=settings.DEFAULT_CURRENCY,
    )
    yield data
