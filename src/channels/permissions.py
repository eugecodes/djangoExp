from model_utils import Choices


class ChannelPermissions:
    CREATE = "add_channel"
    EDIT = "change_channel"
    READ = "view_channel"
    DELETE = "delete_channel"
    PERMISSIONS = Choices(CREATE, EDIT, READ, DELETE)
