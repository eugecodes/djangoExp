import pytest
from ninja.errors import AuthenticationError

from rate_types.services import (
    rate_type_create,
    rate_type_update,
)


@pytest.mark.django_db
def test_create_rate_type_channel_admin(channel_admin, rate_type_create_request):
    with pytest.raises(AuthenticationError):
        rate_type_create(rate_type_create_request, channel_admin)


@pytest.mark.django_db
def test_update_rate_type_channel_admin(
    channel_admin, rate_type, rate_type_update_request
):
    with pytest.raises(AuthenticationError):
        rate_type_update(rate_type, rate_type_update_request, channel_admin)
