from ninja import Schema, ModelSchema
from {{ cookiecutter.app_slug_plural }}.models import {{ cookiecutter.app_name }}


class {{ cookiecutter.app_name }}Request(ModelSchema):
    class Config:
        model = {{ cookiecutter.app_name }}
        model_fields = ["name",]
        optional_fields = []

class {{ cookiecutter.app_name }}UpdateRequest(ModelSchema):
    class Config:
        model = {{ cookiecutter.app_name }}
        model_fields = ["name",]
        optional_fields = []