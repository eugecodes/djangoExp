from ninja import ModelSchema
from {{ cookiecutter.app_slug_plural }}.models import {{ cookiecutter.app_name }}


class Basic{{ cookiecutter.app_name }}Response(ModelSchema):
    class Config:
        model = {{ cookiecutter.app_name }}
        model_fields = ["id", "created"]


class {{ cookiecutter.app_name }}ListResponse(ModelSchema):
    class Config:
        model = {{ cookiecutter.app_name }}
        model_fields = ["id", "created"]


class {{ cookiecutter.app_name }}DetailResponse(ModelSchema):
    class Config:
        model = {{ cookiecutter.app_name }}
        model_fields = ["id", "created"]

