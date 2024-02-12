from django.contrib.auth import get_user_model
from ninja import ModelSchema, Schema

User = get_user_model()


class BasicUserResponse(ModelSchema):
    class Config:
        model = User
        model_fields = ["id", "first_name", "last_name", "created"]


class UserListResponse(ModelSchema):
    class Config:
        model = User
        model_fields = ["id", "first_name", "last_name", "created"]


class UserMeDetailResponse(ModelSchema):
    # email: EmailStr
    # responsible: BasicUserResponse | None

    # create_at: Optional[datetime]
    # is_active: bool
    # is_deleted: bool
    # is_superadmin: bool
    # role: UserRole | None
    class Config:
        model = User
        model_fields = ["id", "first_name", "last_name", "email", "created"]


class UserLoginResponse(Schema):
    token: str
    user: UserMeDetailResponse
