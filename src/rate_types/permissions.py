from model_utils import Choices


class RateTypePermissions:
    CREATE = "rate_types.add_ratetype"
    EDIT = "rate_types.change_ratetype"
    READ = "rate_types.view_ratetype"
    DELETE = "rate_types.delete_ratetype"
    PERMISSIONS = Choices(CREATE, EDIT, READ, DELETE)
