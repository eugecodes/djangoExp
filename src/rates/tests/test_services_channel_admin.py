import pytest
from ninja.errors import AuthenticationError

from rates.services import (
    rate_create,
    rate_update,
)


@pytest.mark.django_db
def test_create_rate_channel_admin(channel_admin, rate_create_request):
    with pytest.raises(AuthenticationError):
        rate_create(rate_create_request, channel_admin)


@pytest.mark.django_db
def test_update_rate_channel_admin(channel_admin, rate, rate_update_request):
    with pytest.raises(AuthenticationError):
        rate_update(rate, rate_update_request, channel_admin)
