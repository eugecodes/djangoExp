from model_utils import Choices


class AddressPermissions:
    CREATE = "addresses.add_address"
    EDIT = "addresses.change_address"
    READ = "addresses.view_address"
    DELETE = "addresses.delete_address"
    PERMISSIONS = Choices(CREATE, EDIT, READ, DELETE)
