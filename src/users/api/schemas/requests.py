from django.contrib.auth import get_user_model
from ninja import Schema, ModelSchema
from pydantic import EmailStr

User = get_user_model()


class UserLoginRequest(Schema):
    email: EmailStr
    password: str


class ForgotPasswordRequest(Schema):
    email: EmailStr


class ResetPasswordRequest(Schema):
    password: str
    user_id: int
    hash: str


class UserCreateRequest(ModelSchema):
    class Config:
        model = User
        model_fields = ["first_name", "last_name", "email", "channel"]


class UserRequest(ModelSchema):
    class Config:
        model = User
        model_fields = ["first_name", "last_name", "email"]
