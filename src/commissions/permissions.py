from model_utils import Choices


class CommissionPermissions:
    CREATE = "commissions.add_commission"
    EDIT = "commissions.change_commission"
    READ = "commissions.view_commission"
    DELETE = "commissions.delete_commission"
    PERMISSIONS = Choices(CREATE, EDIT, READ, DELETE)
