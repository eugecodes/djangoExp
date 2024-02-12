from model_utils import Choices


class OtherCostPermissions:
    CREATE = "costs.add_othercost"
    EDIT = "costs.change_othercost"
    READ = "costs.view_othercost"
    DELETE = "costs.delete_othercost"
    PERMISSIONS = Choices(CREATE, EDIT, READ, DELETE)
