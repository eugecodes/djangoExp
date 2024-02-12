import pytest
from ninja.errors import AuthenticationError

from energy_costs.services import (
    energy_cost_create,
    energy_cost_update,
)


@pytest.mark.django_db
def test_create_energy_cost_channel_admin(channel_admin, energy_cost_create_request):
    with pytest.raises(AuthenticationError):
        energy_cost_create(energy_cost_create_request, channel_admin)


@pytest.mark.django_db
def test_update_energy_cost_channel_admin(
    channel_admin, energy_cost, energy_cost_update_request
):
    with pytest.raises(AuthenticationError):
        energy_cost_update(energy_cost, energy_cost_update_request, channel_admin)
