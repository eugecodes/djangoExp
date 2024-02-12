from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.crypto import get_random_string
from ninja.errors import AuthenticationError

from users.api.schemas.requests import (
    UserLoginRequest,
    ForgotPasswordRequest,
)
from users.models import Token

User = get_user_model()


def get_user_by_token(token: str) -> User:
    return Token.objects.select_related("user").get(token=token).user


def get_or_create_user_token(user: User) -> Token:
    return get_or_create_token(user)


def login_user(login_data: UserLoginRequest) -> Token:
    user = User.objects.get(email=login_data.email)
    try:
        validate_password(login_data.password, user)
    except ValidationError:
        raise AuthenticationError
    token = get_or_create_user_token(user)
    return token


def logout_user(user: User) -> None:
    Token.objects.filter(user=user).delete()


def get_or_create_token(user: User) -> Token:
    token, created = Token.objects.get_or_create(
        user=user, defaults={"token": get_random_string(settings.DEFAULT_TOKEN_LENGTH)}
    )
    return token


def forgot_password(user_email: ForgotPasswordRequest):
    try:
        user = User.objects.get(email=user_email.email)
    except User.DoesNotExist:
        return

    # email_message = EmailMessageSchema(
    #     subject=_("test reset password"),
    #     recipients=[user.email],
    #     parameters={
    #         "content_1": _("Hi"),
    #         "content_2": user.first_name,
    #         "content_3": _("You have requested a password change."),
    #         "content_4": _("to reset your password click on the following link:"),
    #         "content_5": _("Reset password"),
    #         "content_6": _("Thank you."),
    #         "content_7": _("Regards"),
    #     },
    # )
    # verification_account(user, email_message)
