import pytest
from ninja.errors import AuthenticationError

from margins.services import (
    margin_create,
    margin_update,
)


@pytest.mark.django_db
def test_create_margin_channel_admin(channel_admin, margin_create_request):
    with pytest.raises(AuthenticationError):
        margin_create(margin_create_request, channel_admin)


@pytest.mark.django_db
def test_update_margin_channel_admin(channel_admin, margin, margin_update_request):
    with pytest.raises(AuthenticationError):
        margin_update(margin, margin_update_request, channel_admin)
