import pytest

from clients.choices import ClientTypes
from common.choices import EnergyTypes
from saving_studies.api.schemas.requests import (
    SavingStudyRequest,
    SavingStudyUpdateRequest,
)


@pytest.fixture
def saving_study_create_request(rate_type, channel):
    data = SavingStudyRequest(
        name="TestSavingStudy",
        energy_type=EnergyTypes.ELECTRICITY,
        cups="123123123",
        client_type=ClientTypes.COMPANY,
        current_rate_type_id=rate_type.id,
        channel_id=channel.id,
    )
    yield data


@pytest.fixture
def saving_study_update_request(rate_type):
    data = SavingStudyUpdateRequest(
        client_type=ClientTypes.COMPANY,
        current_rate_type_id=rate_type.id,
    )
    yield data
