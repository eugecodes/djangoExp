import pytest

from suggested_rates.api.schemas.requests import SuggestedRateRequest, SuggestedRateUpdateRequest


@pytest.fixture
def suggested_rate_create_request():
    data = SuggestedRateRequest(name="TestSuggestedRate")
    yield data


@pytest.fixture
def suggested_rate_update_request():
    data = SuggestedRateUpdateRequest(name="NewTestSuggestedRate")
    yield data
