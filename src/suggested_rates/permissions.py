from model_utils import Choices


class SuggestedRatePermissions:
    CREATE = "suggested_rates.add_suggestedrate"
    EDIT = "suggested_rates.change_suggestedrate"
    READ = "suggested_rates.view_suggestedrate"
    DELETE = "suggested_rates.delete_suggestedrate"
    PERMISSIONS = Choices(CREATE, EDIT, READ, DELETE)
