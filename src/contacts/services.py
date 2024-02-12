from auditlog.context import set_actor
from django.contrib.auth import get_user_model
from ninja.errors import AuthenticationError
from ninja import FilterSchema
from common.api.requests import DeleteRequest
from common.services import model_update, delete_models, detail_model
from guardian.shortcuts import get_objects_for_user
from contacts.api.schemas.requests import ContactRequest, ContactUpdateRequest
from contacts.permissions import ContactPermissions
from contacts.models import Contact


User = get_user_model()

def contact_list(filters: FilterSchema, actor: User):
    if actor.is_superuser:
        contacts = Contact.objects.all()
    else:
        contacts = get_objects_for_user(actor, ContactPermissions.READ)
    contacts = filters.filter(contacts)
    return contacts


def contact_create(data: ContactRequest, actor: User):
    if not actor.has_perm(ContactPermissions.CREATE) and not actor.is_superuser:
        raise AuthenticationError
    with set_actor(actor):
        contact = Contact.objects.create(**data.dict())
    return contact


def contact_update(contact: Contact, data: ContactUpdateRequest, actor: User) -> Contact:
    if not actor.has_perm(ContactPermissions.EDIT, contact) and not actor.is_superuser:
        raise AuthenticationError
    return model_update(contact, data, actor)


def contact_detail(contact: Contact, actor: User) -> Contact:
    return detail_model(actor, ContactPermissions.READ, contact)


def delete_contacts(data: DeleteRequest, actor: User):
    delete_models(actor, ContactPermissions.DELETE, data)
