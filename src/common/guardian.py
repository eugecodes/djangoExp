from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


def get_anonymous_user_instance(User):
    return User(email=settings.ANONYMOUS_EMAIL)
