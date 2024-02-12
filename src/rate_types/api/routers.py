from typing import List

from django.http import FileResponse
from django.shortcuts import get_object_or_404
from ninja import Router, Query
from ninja.pagination import paginate

from common.api.requests import DeleteRequest
from common.export import generate_csv_file
from common.pagination import CustomPagination
from rate_types.api.schemas.exports import rate_type_export_headers
from rate_types.api.schemas.filters import RateTypeFilterSchema
from rate_types.api.schemas.requests import RateTypeRequest
from rate_types.api.schemas.responses import (
    RateTypeListResponse,
    BasicRateTypeResponse,
)
from rate_types.models import RateType
from rate_types.services import (
    rate_type_create,
    rate_type_update,
    delete_rate_types,
    rate_types_list,
    rate_type_detail,
)

router = Router()


@router.get("", response=List[RateTypeListResponse])
@paginate(CustomPagination)
def rate_type_list_endpoint(request, filters: RateTypeFilterSchema = Query(...)):
    return rate_types_list(filters, request.user)


@router.post("", response={201: BasicRateTypeResponse})
def rate_type_create_endpoint(request, payload: RateTypeRequest):
    return rate_type_create(payload, request.user)


@router.put("/{rate_type_id}", response=BasicRateTypeResponse)
def rate_type_update_endpoint(request, rate_type_id: int, payload: RateTypeRequest):
    rate_type = get_object_or_404(RateType, id=rate_type_id)
    return rate_type_update(rate_type, payload, request.user)


@router.patch("/{rate_type_id}", response=BasicRateTypeResponse)
def rate_type_update_partial_endpoint(
    request, rate_type_id: int, payload: RateTypeRequest
):
    rate_type = get_object_or_404(RateType, id=rate_type_id)
    return rate_type_update(rate_type, payload, request.user)


@router.get("/{rate_type_id}", response=BasicRateTypeResponse)
def rate_type_detail_endpoint(request, rate_type_id: int):
    rate_type = get_object_or_404(RateType, id=rate_type_id)
    return rate_type_detail(rate_type, request.user)


@router.post("/delete/")
def delete_rate_type_endpoint(request, payload: DeleteRequest):
    delete_rate_types(payload, request.user)


@router.post("/export/csv/")
def rate_type_export_endpoint(request):
    return FileResponse(
        generate_csv_file("rate_type", rate_type_export_headers, RateType.objects.all())
    )
