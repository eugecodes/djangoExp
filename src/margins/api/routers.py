from typing import List

from django.http import FileResponse
from django.shortcuts import get_object_or_404
from ninja import Router, Query
from ninja.pagination import paginate

from common.api.requests import DeleteRequest
from common.export import generate_csv_file
from common.pagination import CustomPagination
from margins.api.schemas.exports import margin_export_headers
from margins.api.schemas.filters import MarginFilterSchema
from margins.api.schemas.requests import MarginRequest, MarginUpdateRequest
from margins.api.schemas.responses import (
    MarginListResponse,
    BasicMarginResponse,
)
from margins.models import Margin
from margins.services import (
    margin_create,
    margin_update,
    delete_margins,
    margin_detail,
    margin_list,
)

router = Router()


@router.get("", response=List[MarginListResponse])
@paginate(CustomPagination)
def margin_list_endpoint(request, filters: MarginFilterSchema = Query(...)):
    return margin_list(filters, request.user)


@router.post("", response={201: BasicMarginResponse})
def margin_create_endpoint(request, payload: MarginRequest):
    return margin_create(payload, request.user)


@router.put("/{margin_id}", response=BasicMarginResponse)
def margin_update_endpoint(request, margin_id: int, payload: MarginUpdateRequest):
    margin = get_object_or_404(Margin, id=margin_id)
    return margin_update(margin, payload, request.user)


@router.patch("/{margin_id}", response=BasicMarginResponse)
def margin_update_partial_endpoint(
    request, margin_id: int, payload: MarginUpdateRequest
):
    margin = get_object_or_404(Margin, id=margin_id)
    return margin_update(margin, payload, request.user)


@router.get("/{margin_id}", response=BasicMarginResponse)
def margin_detail_endpoint(request, margin_id: int):
    margin = get_object_or_404(Margin, id=margin_id)
    return margin_detail(margin, request.user)


@router.post("/delete/")
def delete_margin_endpoint(request, payload: DeleteRequest):
    delete_margins(payload, request.user)


@router.post("/export/csv/")
def margin_export_endpoint(request):
    return FileResponse(
        generate_csv_file("margin", margin_export_headers, Margin.objects.all())
    )
