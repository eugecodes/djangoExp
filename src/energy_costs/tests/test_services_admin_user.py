import pytest

from energy_costs.services import (
    energy_cost_create,
    energy_cost_update,
)


@pytest.mark.django_db
def test_create_energy_cost_admin_user(admin_user, energy_cost_create_request):
    new_energy_cost = energy_cost_create(energy_cost_create_request, admin_user)
    assert new_energy_cost.code == energy_cost_create_request.code


@pytest.mark.django_db
def test_update_energy_cost_admin_user(
    admin_user, energy_cost, energy_cost_update_request
):
    updatable_energy_cost = energy_cost_update(
        energy_cost, energy_cost_update_request, admin_user
    )
    assert updatable_energy_cost.code == energy_cost_update_request.code
