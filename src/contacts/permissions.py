from model_utils import Choices


class ContactPermissions:
    CREATE = "contacts.add_contact"
    EDIT = "contacts.change_contact"
    READ = "contacts.view_contact"
    DELETE = "contacts.delete_contact"
    PERMISSIONS = Choices(CREATE, EDIT, READ, DELETE)
