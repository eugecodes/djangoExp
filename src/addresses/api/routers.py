from typing import List

from django.http import FileResponse
from django.shortcuts import get_object_or_404
from ninja import Router, Query
from ninja.pagination import paginate

from common.api.requests import DeleteRequest
from common.export import generate_csv_file
from common.pagination import CustomPagination
from addresses.api.schemas.exports import address_export_headers
from addresses.api.schemas.requests import AddressRequest, AddressUpdateRequest
from addresses.api.schemas.filters import AddressFilterSchema
from addresses.api.schemas.responses import (
    AddressListResponse,
    BasicAddressResponse,
)
from addresses.services import (
    address_create,
    address_update,
    delete_addresses,
    address_list,
    address_detail,
)
from addresses.models import Address

router = Router()


@router.get("", response=List[AddressListResponse])
@paginate(CustomPagination)
def address_list_endpoint(request, filters: AddressFilterSchema = Query(...)):
    return address_list(filters, request.user)


@router.post("", response={201: BasicAddressResponse})
def address_create_endpoint(request, payload: AddressRequest):
    return address_create(payload, request.user)


@router.put("/{address_id}", response=BasicAddressResponse)
def address_update_endpoint(request, address_id: int, payload: AddressUpdateRequest):
    address = get_object_or_404(Address, id=address_id)
    return address_update(address, payload, request.user)


@router.patch("/{address_id}", response=BasicAddressResponse)
def address_update_partial_endpoint(request, address_id: int, payload: AddressUpdateRequest):
    address = get_object_or_404(Address, id=address_id)
    return address_update(address, payload, request.user)


@router.get("/{address_id}", response=BasicAddressResponse)
def address_detail_endpoint(request, address_id: int):
    address = get_object_or_404(Address, id=address_id)
    return address_detail(address, request.user)


@router.post("/delete/")
def delete_address_endpoint(request, payload: DeleteRequest):
    delete_addresses(payload, request.user)


@router.post("/export/csv/")
def address_export_endpoint(request):
    return FileResponse(
        generate_csv_file("address", address_export_headers, Address.objects.all())
    )
