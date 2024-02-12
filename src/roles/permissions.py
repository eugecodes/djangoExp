from model_utils import Choices


class RolePermissions:
    CREATE = "roles.add_role"
    EDIT = "roles.change_role"
    READ = "roles.view_role"
    DELETE = "roles.delete_role"
    PERMISSIONS = Choices(CREATE, EDIT, READ, DELETE)
