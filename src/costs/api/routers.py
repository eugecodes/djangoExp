from typing import List

from django.http import FileResponse
from django.shortcuts import get_object_or_404
from ninja import Router, Query
from ninja.pagination import paginate

from common.api.requests import DeleteRequest
from common.export import generate_csv_file
from common.pagination import CustomPagination
from costs.api.schemas.exports import cost_export_headers
from costs.api.schemas.requests import OtherCostRequest, OtherCostUpdateRequest
from costs.api.schemas.filters import OtherCostFilterSchema
from costs.api.schemas.responses import (
    OtherCostListResponse,
    BasicOtherCostResponse,
)
from costs.services import (
    cost_create,
    cost_update,
    delete_costs,
    cost_list,
    cost_detail,
)
from costs.models import OtherCost

router = Router()


@router.get("", response=List[OtherCostListResponse])
@paginate(CustomPagination)
def cost_list_endpoint(request, filters: OtherCostFilterSchema = Query(...)):
    return cost_list(filters, request.user)


@router.post("", response={201: BasicOtherCostResponse})
def cost_create_endpoint(request, payload: OtherCostRequest):
    return cost_create(payload, request.user)


@router.put("/{cost_id}", response=BasicOtherCostResponse)
def cost_update_endpoint(request, cost_id: int, payload: OtherCostUpdateRequest):
    cost = get_object_or_404(OtherCost, id=cost_id)
    return cost_update(cost, payload, request.user)


@router.patch("/{cost_id}", response=BasicOtherCostResponse)
def cost_update_partial_endpoint(request, cost_id: int, payload: OtherCostUpdateRequest):
    cost = get_object_or_404(OtherCost, id=cost_id)
    return cost_update(cost, payload, request.user)


@router.get("/{cost_id}", response=BasicOtherCostResponse)
def cost_detail_endpoint(request, cost_id: int):
    cost = get_object_or_404(OtherCost, id=cost_id)
    return cost_detail(cost, request.user)


@router.post("/delete/")
def delete_cost_endpoint(request, payload: DeleteRequest):
    delete_costs(payload, request.user)


@router.post("/export/csv/")
def cost_export_endpoint(request):
    return FileResponse(
        generate_csv_file("cost", cost_export_headers, OtherCost.objects.all())
    )
