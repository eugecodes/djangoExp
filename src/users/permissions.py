from model_utils import Choices


class UserPermissions:
    CREATE = "users.add_user"
    EDIT = "users.change_user"
    READ = "users.view_user"
    DELETE = "users.delete_user"
    PERMISSIONS = Choices(CREATE, EDIT, READ, DELETE)
