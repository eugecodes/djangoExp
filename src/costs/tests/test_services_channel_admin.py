import pytest
from ninja.errors import AuthenticationError

from costs.services import (
    cost_create,
    cost_update,
)


@pytest.mark.django_db
def test_create_cost_channel_admin(channel_admin, cost_create_request):
    with pytest.raises(AuthenticationError):
        cost_create(cost_create_request, channel_admin)


@pytest.mark.django_db
def test_update_cost_channel_admin(channel_admin, cost, cost_update_request):
    with pytest.raises(AuthenticationError):
        cost_update(cost, cost_update_request, channel_admin)
