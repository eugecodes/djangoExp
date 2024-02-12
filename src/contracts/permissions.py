from model_utils import Choices


class ContractPermissions:
    CREATE = "contracts.add_contract"
    EDIT = "contracts.change_contract"
    READ = "contracts.view_contract"
    DELETE = "contracts.delete_contract"
    PERMISSIONS = Choices(CREATE, EDIT, READ, DELETE)
