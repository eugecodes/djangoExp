from model_utils import Choices


class InvoicePermissions:
    CREATE = "invoices.add_invoice"
    EDIT = "invoices.change_invoice"
    READ = "invoices.view_invoice"
    DELETE = "invoices.delete_invoice"
    PERMISSIONS = Choices(CREATE, EDIT, READ, DELETE)
