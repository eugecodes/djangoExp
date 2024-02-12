from typing import List

from django.http import FileResponse
from django.shortcuts import get_object_or_404
from ninja import Router, Query
from ninja.pagination import paginate

from common.api.requests import DeleteRequest
from common.export import generate_csv_file
from common.pagination import CustomPagination
from rates.api.schemas.exports import rate_export_headers
from rates.api.schemas.filters import RateFilterSchema
from rates.api.schemas.requests import RateRequest, RateUpdateRequest
from rates.api.schemas.responses import (
    RateListResponse,
    BasicRateResponse,
)
from rates.models import Rate
from rates.services import (
    rate_create,
    rate_update,
    delete_rates,
    rate_list,
    rate_detail,
)

router = Router()


@router.get("", response=List[RateListResponse])
@paginate(CustomPagination)
def rate_list_endpoint(request, filters: RateFilterSchema = Query(...)):
    return rate_list(filters, request.user)


@router.post("", response={201: BasicRateResponse})
def rate_create_endpoint(request, payload: RateRequest):
    return rate_create(payload, request.user)


@router.put("/{rate_id}", response=BasicRateResponse)
def rate_update_endpoint(request, rate_id: int, payload: RateUpdateRequest):
    rate = get_object_or_404(Rate, id=rate_id)
    return rate_update(rate, payload, request.user)


@router.patch("/{rate_id}", response=BasicRateResponse)
def rate_update_partial_endpoint(request, rate_id: int, payload: RateUpdateRequest):
    rate = get_object_or_404(Rate, id=rate_id)
    return rate_update(rate, payload, request.user)


@router.get("/{rate_id}", response=BasicRateResponse)
def rate_detail_endpoint(request, rate_id: int):
    rate = get_object_or_404(Rate, id=rate_id)
    return rate_detail(rate, request.user)


@router.post("/delete/")
def delete_rate_endpoint(request, payload: DeleteRequest):
    delete_rates(payload, request.user)


@router.post("/export/csv/")
def rate_export_endpoint(request):
    return FileResponse(
        generate_csv_file("rate", rate_export_headers, Rate.objects.all())
    )
