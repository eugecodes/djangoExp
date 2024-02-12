from typing import List

from django.http import FileResponse
from django.shortcuts import get_object_or_404
from ninja import Router, Query
from ninja.pagination import paginate

from common.api.requests import DeleteRequest
from common.export import generate_csv_file
from common.pagination import CustomPagination
from marketers.api.schemas.exports import marketer_export_headers
from marketers.api.schemas.filters import MarketerFilterSchema
from marketers.api.schemas.requests import MarketerRequest
from marketers.api.schemas.responses import (
    MarketerListResponse,
    BasicMarketerResponse,
)
from marketers.models import Marketer
from marketers.services import (
    marketer_create,
    marketer_update,
    delete_marketers,
    marketer_list,
    marketer_detail,
)

router = Router()


@router.get("", response=List[MarketerListResponse])
@paginate(CustomPagination)
def marketer_list_endpoint(request, filters: MarketerFilterSchema = Query(...)):
    return marketer_list(filters, request.user)


@router.post("", response={201: BasicMarketerResponse})
def marketer_create_endpoint(request, payload: MarketerRequest):
    return marketer_create(payload, request.user)


@router.put("/{marketer_id}", response=BasicMarketerResponse)
def marketer_update_endpoint(request, marketer_id: int, payload: MarketerRequest):
    marketer = get_object_or_404(Marketer, id=marketer_id)
    return marketer_update(marketer, payload, request.user)


@router.patch("/{marketer_id}", response=BasicMarketerResponse)
def marketer_update_partial_endpoint(
    request, marketer_id: int, payload: MarketerRequest
):
    marketer = get_object_or_404(Marketer, id=marketer_id)
    return marketer_update(marketer, payload, request.user)


@router.get("/{marketer_id}", response=BasicMarketerResponse)
def marketer_detail_endpoint(request, marketer_id: int):
    marketer = get_object_or_404(Marketer, id=marketer_id)
    return marketer_detail(marketer, request.user)


@router.post("/delete/")
def delete_marketer_endpoint(request, payload: DeleteRequest):
    delete_marketers(payload, request.user)


@router.post("/export/csv/")
def marketer_export_endpoint(request):
    return FileResponse(
        generate_csv_file("marketer", marketer_export_headers, Marketer.objects.all())
    )
