from typing import List

from django.http import FileResponse
from django.shortcuts import get_object_or_404
from ninja import Router, Query
from ninja.pagination import paginate

from clients.api.schemas.exports import client_export_headers
from clients.api.schemas.filters import ClientFilterSchema
from clients.api.schemas.requests import ClientRequest, ClientUpdateRequest
from clients.api.schemas.responses import (
    ClientListResponse,
    BasicClientResponse,
)
from clients.models import Client
from clients.services import (
    client_create,
    client_update,
    delete_clients,
    client_list,
    client_detail,
)
from common.api.requests import DeleteRequest
from common.export import generate_csv_file
from common.pagination import CustomPagination

router = Router()


@router.get("", response=List[ClientListResponse])
@paginate(CustomPagination)
def client_list_endpoint(request, filters: ClientFilterSchema = Query(...)):
    return client_list(filters, request.user)


@router.post("", response={201: BasicClientResponse})
def client_create_endpoint(request, payload: ClientRequest):
    return client_create(payload, request.user)


@router.put("/{client_id}", response=BasicClientResponse)
def client_update_endpoint(request, client_id: int, payload: ClientUpdateRequest):
    client = get_object_or_404(Client, id=client_id)
    return client_update(client, payload, request.user)


@router.patch("/{client_id}", response=BasicClientResponse)
def client_update_partial_endpoint(
    request, client_id: int, payload: ClientUpdateRequest
):
    client = get_object_or_404(Client, id=client_id)
    return client_update(client, payload, request.user)


@router.get("/{client_id}", response=BasicClientResponse)
def client_detail_endpoint(request, client_id: int):
    client = get_object_or_404(Client, id=client_id)
    return client_detail(client, request.user)


@router.post("/delete/")
def delete_client_endpoint(request, payload: DeleteRequest):
    delete_clients(payload, request.user)


@router.post("/export/csv/")
def client_export_endpoint(request):
    return FileResponse(
        generate_csv_file("client", client_export_headers, Client.objects.all())
    )
