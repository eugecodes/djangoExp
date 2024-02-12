import pytest
from ninja.errors import AuthenticationError
from guardian.shortcuts import assign_perm
from commissions.permissions import CommissionPermissions
from commissions.services import (
    commission_create,
    commission_update,
)


@pytest.mark.django_db
def test_create_commission_channel_user_not_allowed(channel_user, commission_create_request):
    with pytest.raises(AuthenticationError):
        commission_create(commission_create_request, channel_user)

@pytest.mark.django_db
def test_create_commission_channel_user_allowed(channel_user, commission_create_request):
    assign_perm(CommissionPermissions.CREATE, channel_user)
    new_commission = commission_create(commission_create_request, channel_user)
    assert new_commission.name == commission_create_request.name


@pytest.mark.django_db
def test_update_commission_channel_user_not_allowed(channel_user, commission, commission_update_request):
    with pytest.raises(AuthenticationError):
        commission_update(commission, commission_update_request, channel_user)


@pytest.mark.django_db
def test_update_commission_channel_user_allowed(channel_user, commission, commission_update_request):
    assign_perm(CommissionPermissions.EDIT, channel_user, commission)
    updatable_commission = commission_update(commission, commission_update_request, channel_user)
    assert updatable_commission.name == commission_update_request.name