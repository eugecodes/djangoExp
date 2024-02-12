from model_utils import Choices


class ClientPermissions:
    CREATE = "clients.add_client"
    EDIT = "clients.change_client"
    READ = "clients.view_client"
    DELETE = "clients.delete_client"
    PERMISSIONS = Choices(CREATE, EDIT, READ, DELETE)
