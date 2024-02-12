from typing import List

from django.http import FileResponse
from django.shortcuts import get_object_or_404
from ninja import Router, Query
from ninja.pagination import paginate

from common.api.requests import DeleteRequest
from common.export import generate_csv_file
from common.pagination import CustomPagination
from suggested_rates.api.schemas.exports import suggested_rate_export_headers
from suggested_rates.api.schemas.filters import SuggestedRateFilterSchema
from suggested_rates.api.schemas.requests import (
    SuggestedRateRequest,
    SuggestedRateUpdateRequest,
)
from suggested_rates.api.schemas.responses import (
    SuggestedRateListResponse,
    BasicSuggestedRateResponse,
)
from suggested_rates.models import SuggestedRate
from suggested_rates.services.base import (
    suggested_rate_create,
    suggested_rate_update,
    delete_suggested_rates,
    suggested_rate_list,
    suggested_rate_detail,
)

router = Router()


@router.get("", response=List[SuggestedRateListResponse])
@paginate(CustomPagination)
def suggested_rate_list_endpoint(
    request, filters: SuggestedRateFilterSchema = Query(...)
):
    return suggested_rate_list(filters, request.user)


@router.post("", response={201: BasicSuggestedRateResponse})
def suggested_rate_create_endpoint(request, payload: SuggestedRateRequest):
    return suggested_rate_create(payload, request.user)


@router.put("/{suggested_rate_id}", response=BasicSuggestedRateResponse)
def suggested_rate_update_endpoint(
    request, suggested_rate_id: int, payload: SuggestedRateUpdateRequest
):
    suggested_rate = get_object_or_404(SuggestedRate, id=suggested_rate_id)
    return suggested_rate_update(suggested_rate, payload, request.user)


@router.patch("/{suggested_rate_id}", response=BasicSuggestedRateResponse)
def suggested_rate_update_partial_endpoint(
    request, suggested_rate_id: int, payload: SuggestedRateUpdateRequest
):
    suggested_rate = get_object_or_404(SuggestedRate, id=suggested_rate_id)
    return suggested_rate_update(suggested_rate, payload, request.user)


@router.get("/{suggested_rate_id}", response=BasicSuggestedRateResponse)
def suggested_rate_detail_endpoint(request, suggested_rate_id: int):
    suggested_rate = get_object_or_404(SuggestedRate, id=suggested_rate_id)
    return suggested_rate_detail(suggested_rate, request.user)


@router.post("/delete/")
def delete_suggested_rate_endpoint(request, payload: DeleteRequest):
    delete_suggested_rates(payload, request.user)


@router.post("/export/csv/")
def suggested_rate_export_endpoint(request):
    return FileResponse(
        generate_csv_file(
            "suggested_rate", suggested_rate_export_headers, SuggestedRate.objects.all()
        )
    )
