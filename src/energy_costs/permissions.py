from model_utils import Choices


class EnergyCostPermissions:
    CREATE = "energy_costs.add_energycost"
    EDIT = "energy_costs.change_energycost"
    READ = "energy_costs.view_energycost"
    DELETE = "energy_costs.delete_energycost"
    PERMISSIONS = Choices(CREATE, EDIT, READ, DELETE)
