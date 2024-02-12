import pytest

from costs.services import (
    cost_create,
    cost_update,
)


@pytest.mark.django_db
def test_create_cost_admin_user(admin_user, cost_create_request):
    new_cost = cost_create(cost_create_request, admin_user)
    assert new_cost.name == cost_create_request.name


@pytest.mark.django_db
def test_update_cost_admin_user(admin_user, cost, cost_update_request):
    updatable_cost = cost_update(cost, cost_update_request, admin_user)
    assert updatable_cost.name == cost_update_request.name
