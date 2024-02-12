import pytest
from ninja.errors import AuthenticationError
from guardian.shortcuts import assign_perm
from costs.permissions import OtherCostPermissions
from costs.services import (
    cost_create,
    cost_update,
)


@pytest.mark.django_db
def test_create_cost_channel_user_not_allowed(channel_user, cost_create_request):
    with pytest.raises(AuthenticationError):
        cost_create(cost_create_request, channel_user)

@pytest.mark.django_db
def test_create_cost_channel_user_allowed(channel_user, cost_create_request):
    assign_perm(OtherCostPermissions.CREATE, channel_user)
    new_cost = cost_create(cost_create_request, channel_user)
    assert new_cost.name == cost_create_request.name


@pytest.mark.django_db
def test_update_cost_channel_user_not_allowed(channel_user, cost, cost_update_request):
    with pytest.raises(AuthenticationError):
        cost_update(cost, cost_update_request, channel_user)


@pytest.mark.django_db
def test_update_cost_channel_user_allowed(channel_user, cost, cost_update_request):
    assign_perm(OtherCostPermissions.EDIT, channel_user, cost)
    updatable_cost = cost_update(cost, cost_update_request, channel_user)
    assert updatable_cost.name == cost_update_request.name