from typing import Any

from django.contrib.auth import get_user_model
from ninja.testing import TestClient

from config.api import api
from users.services.login import get_or_create_token

User = get_user_model()


class CustomTestClient(TestClient):
    token: str

    def set_user(self, user: User):
        token = get_or_create_token(user)
        self.token = token.token

    def request(self, method, path, data={}, json=None, **request_params: Any):
        if self.token is not None:
            headers = {"Authorization": f"token {self.token}"}
            request_params["headers"] = headers
        return super().request(method, path, data, json, **request_params)


client = CustomTestClient(api)
