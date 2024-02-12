import pytest
from ninja.errors import AuthenticationError

from commissions.services import (
    commission_create,
    commission_update,
)


@pytest.mark.django_db
def test_create_commission_channel_admin(channel_admin, commission_create_request):
    with pytest.raises(AuthenticationError):
        commission_create(commission_create_request, channel_admin)


@pytest.mark.django_db
def test_update_commission_channel_admin(
    channel_admin, commission, commission_update_request
):
    with pytest.raises(AuthenticationError):
        commission_update(commission, commission_update_request, channel_admin)
