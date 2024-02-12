import pytest

from commissions.api.schemas.requests import CommissionRequest, CommissionUpdateRequest


@pytest.fixture
def commission_create_request(rate_type):
    data = CommissionRequest(
        name="TestCommission",
        min_consumption=1.1,
        max_consumption=1.1,
        percentage_test_commission=1,
        rate_type_id=rate_type.id,
        # rates=[5],
    )
    yield data


@pytest.fixture
def commission_update_request():
    data = CommissionUpdateRequest(
        name="NewTestCommission",
        min_consumption=1.1,
        max_consumption=1.1,
        percentage_test_commission=1,
        # rates=[5],
    )
    yield data
