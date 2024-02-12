import pytest

from margins.services import (
    margin_create,
    margin_update,
)


@pytest.mark.django_db
def test_create_margin_admin_user(admin_user, margin_create_request):
    new_margin = margin_create(margin_create_request, admin_user)
    assert new_margin.type == margin_create_request.type


@pytest.mark.django_db
def test_update_margin_admin_user(admin_user, margin, margin_update_request):
    updatable_margin = margin_update(margin, margin_update_request, admin_user)
    assert updatable_margin.type == margin_update_request.type
