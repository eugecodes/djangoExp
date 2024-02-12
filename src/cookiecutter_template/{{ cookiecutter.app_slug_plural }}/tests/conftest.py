import pytest

from {{ cookiecutter.app_slug_plural }}.api.schemas.requests import {{ cookiecutter.app_name }}Request, {{ cookiecutter.app_name }}UpdateRequest


@pytest.fixture
def {{ cookiecutter.app_slug }}_create_request():
    data = {{ cookiecutter.app_name }}Request(name="Test{{ cookiecutter.app_name }}")
    yield data


@pytest.fixture
def {{ cookiecutter.app_slug }}_update_request():
    data = {{ cookiecutter.app_name }}UpdateRequest(name="NewTest{{ cookiecutter.app_name }}")
    yield data
