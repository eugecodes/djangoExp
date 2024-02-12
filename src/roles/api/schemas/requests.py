from ninja import ModelSchema

from roles.models import Role


class RoleRequest(ModelSchema):
    class Config:
        model = Role
        model_fields = ["name", "channel"]
