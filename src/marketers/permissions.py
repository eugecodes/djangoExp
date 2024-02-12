from model_utils import Choices


class MarketerPermissions:
    CREATE = "marketers.add_marketer"
    EDIT = "marketers.change_marketer"
    READ = "marketers.view_marketer"
    DELETE = "marketers.delete_marketer"
    PERMISSIONS = Choices(CREATE, EDIT, READ, DELETE)
