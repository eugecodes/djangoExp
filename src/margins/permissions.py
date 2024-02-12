from model_utils import Choices


class MarginPermissions:
    CREATE = "margins.add_margin"
    EDIT = "margins.change_margin"
    READ = "margins.view_margin"
    DELETE = "margins.delete_margin"
    PERMISSIONS = Choices(CREATE, EDIT, READ, DELETE)
