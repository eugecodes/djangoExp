import pytest

from roles.api.schemas.requests import RoleRequest


@pytest.fixture
def role_create_request():
    data = RoleRequest(name="TestRol", channel=None)
    yield data


@pytest.fixture
def role_update_request():
    data = RoleRequest(name="NewTestRol")
    yield data
