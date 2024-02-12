from typing import List

from django.http import FileResponse
from django.shortcuts import get_object_or_404
from ninja import Router, Query
from ninja.pagination import paginate

from common.api.requests import DeleteRequest
from common.export import generate_csv_file
from common.pagination import CustomPagination
from contacts.api.schemas.exports import contact_export_headers
from contacts.api.schemas.requests import ContactRequest, ContactUpdateRequest
from contacts.api.schemas.filters import ContactFilterSchema
from contacts.api.schemas.responses import (
    ContactListResponse,
    BasicContactResponse,
)
from contacts.services import (
    contact_create,
    contact_update,
    delete_contacts,
    contact_list,
    contact_detail,
)
from contacts.models import Contact

router = Router()


@router.get("", response=List[ContactListResponse])
@paginate(CustomPagination)
def contact_list_endpoint(request, filters: ContactFilterSchema = Query(...)):
    return contact_list(filters, request.user)


@router.post("", response={201: BasicContactResponse})
def contact_create_endpoint(request, payload: ContactRequest):
    return contact_create(payload, request.user)


@router.put("/{contact_id}", response=BasicContactResponse)
def contact_update_endpoint(request, contact_id: int, payload: ContactUpdateRequest):
    contact = get_object_or_404(Contact, id=contact_id)
    return contact_update(contact, payload, request.user)


@router.patch("/{contact_id}", response=BasicContactResponse)
def contact_update_partial_endpoint(request, contact_id: int, payload: ContactUpdateRequest):
    contact = get_object_or_404(Contact, id=contact_id)
    return contact_update(contact, payload, request.user)


@router.get("/{contact_id}", response=BasicContactResponse)
def contact_detail_endpoint(request, contact_id: int):
    contact = get_object_or_404(Contact, id=contact_id)
    return contact_detail(contact, request.user)


@router.post("/delete/")
def delete_contact_endpoint(request, payload: DeleteRequest):
    delete_contacts(payload, request.user)


@router.post("/export/csv/")
def contact_export_endpoint(request):
    return FileResponse(
        generate_csv_file("contact", contact_export_headers, Contact.objects.all())
    )
