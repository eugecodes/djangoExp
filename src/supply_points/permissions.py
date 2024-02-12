from model_utils import Choices


class SupplyPointPermissions:
    CREATE = "supply_points.add_supplypoint"
    EDIT = "supply_points.change_supplypoint"
    READ = "supply_points.view_supplypoint"
    DELETE = "supply_points.delete_supplypoint"
    PERMISSIONS = Choices(CREATE, EDIT, READ, DELETE)
