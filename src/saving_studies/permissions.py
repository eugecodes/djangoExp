from model_utils import Choices


class SavingStudyPermissions:
    CREATE = "saving_studies.add_savingstudy"
    EDIT = "saving_studies.change_savingstudy"
    READ = "saving_studies.view_savingstudy"
    DELETE = "saving_studies.delete_savingstudy"
    PERMISSIONS = Choices(CREATE, EDIT, READ, DELETE)
