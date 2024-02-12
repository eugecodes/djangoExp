import pytest

from margins.api.schemas.requests import MarginRequest, MarginUpdateRequest
from margins.choices import MarginType


@pytest.fixture
def margin_create_request(rate):
    data = MarginRequest(
        type=MarginType.CONSUME_RANGE,
        min_consumption=1,
        max_consumption=2,
        min_margin=1,
        max_margin=2,
        rate_id=rate.id,
    )
    yield data


@pytest.fixture
def margin_update_request():
    data = MarginUpdateRequest(
        type=MarginType.CONSUME_RANGE,
        min_consumption=1,
        max_consumption=2,
        min_margin=1,
        max_margin=2,
    )
    yield data
