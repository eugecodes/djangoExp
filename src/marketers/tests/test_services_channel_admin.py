import pytest
from ninja.errors import AuthenticationError

from marketers.services import (
    marketer_create,
    marketer_update,
)


@pytest.mark.django_db
def test_create_marketer_channel_admin(channel_admin, marketer_create_request):
    with pytest.raises(AuthenticationError):
        marketer_create(marketer_create_request, channel_admin)


@pytest.mark.django_db
def test_update_marketer_channel_admin(
    channel_admin, marketer, marketer_update_request
):
    with pytest.raises(AuthenticationError):
        marketer_update(marketer, marketer_update_request, channel_admin)
