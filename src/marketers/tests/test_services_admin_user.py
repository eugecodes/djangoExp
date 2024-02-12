import pytest

from marketers.services import (
    marketer_create,
    marketer_update,
)


@pytest.mark.django_db
def test_create_marketer_admin_user(admin_user, marketer_create_request):
    new_marketer = marketer_create(marketer_create_request, admin_user)
    assert new_marketer.name == marketer_create_request.name


@pytest.mark.django_db
def test_update_marketer_admin_user(admin_user, marketer, marketer_update_request):
    updatable_marketer = marketer_update(marketer, marketer_update_request, admin_user)
    assert updatable_marketer.name == marketer_update_request.name
