from ninja import ModelSchema

from roles.models import Role


class BasicRoleResponse(ModelSchema):
    class Config:
        model = Role
        model_fields = ["id", "name", "created"]


class RoleListResponse(ModelSchema):
    class Config:
        model = Role
        model_fields = ["id", "name", "created"]


class RoleDetailResponse(ModelSchema):
    class Config:
        model = Role
        model_fields = ["id", "name", "created"]
