from model_utils import Choices


class RatePermissions:
    CREATE = "rates.add_rate"
    EDIT = "rates.change_rate"
    READ = "rates.view_rate"
    DELETE = "rates.delete_rate"
    PERMISSIONS = Choices(CREATE, EDIT, READ, DELETE)
