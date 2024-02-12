from django.contrib.auth import get_user_model
from django.contrib.auth.forms import BaseUserCreationForm
from django.forms import EmailField

User = get_user_model()


class UserCreationForm(BaseUserCreationForm):
    class Meta:
        model = User
        fields = ("email",)
        field_classes = {"email": EmailField}
