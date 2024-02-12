from model_utils import Choices


class {{ cookiecutter.app_name }}Permissions:
    CREATE = "{{ cookiecutter.app_slug_plural }}.add_{{ cookiecutter.app_slug }}"
    EDIT = "{{ cookiecutter.app_slug_plural }}.change_{{ cookiecutter.app_slug }}"
    READ = "{{ cookiecutter.app_slug_plural }}.view_{{ cookiecutter.app_slug }}"
    DELETE = "{{ cookiecutter.app_slug_plural }}.delete_{{ cookiecutter.app_slug }}"
    PERMISSIONS = Choices(CREATE, EDIT, READ, DELETE)
