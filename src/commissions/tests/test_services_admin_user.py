import pytest

from commissions.services import (
    commission_create,
    commission_update,
)


@pytest.mark.django_db
def test_create_commission_admin_user(admin_user, commission_create_request):
    new_commission = commission_create(commission_create_request, admin_user)
    assert new_commission.name == commission_create_request.name


@pytest.mark.django_db
def test_update_commission_admin_user(admin_user, commission, commission_update_request):
    updatable_commission = commission_update(commission, commission_update_request, admin_user)
    assert updatable_commission.name == commission_update_request.name
