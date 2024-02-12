from typing import List

from django.http import FileResponse
from django.shortcuts import get_object_or_404
from ninja import Router, Query
from ninja.pagination import paginate

from common.api.requests import DeleteRequest
from common.export import generate_csv_file
from common.pagination import CustomPagination
from supply_points.api.schemas.exports import supply_point_export_headers
from supply_points.api.schemas.requests import SupplyPointRequest, SupplyPointUpdateRequest
from supply_points.api.schemas.filters import SupplyPointFilterSchema
from supply_points.api.schemas.responses import (
    SupplyPointListResponse,
    BasicSupplyPointResponse,
)
from supply_points.services import (
    supply_point_create,
    supply_point_update,
    delete_supply_points,
    supply_point_list,
    supply_point_detail,
)
from supply_points.models import SupplyPoint

router = Router()


@router.get("", response=List[SupplyPointListResponse])
@paginate(CustomPagination)
def supply_point_list_endpoint(request, filters: SupplyPointFilterSchema = Query(...)):
    return supply_point_list(filters, request.user)


@router.post("", response={201: BasicSupplyPointResponse})
def supply_point_create_endpoint(request, payload: SupplyPointRequest):
    return supply_point_create(payload, request.user)


@router.put("/{supply_point_id}", response=BasicSupplyPointResponse)
def supply_point_update_endpoint(request, supply_point_id: int, payload: SupplyPointUpdateRequest):
    supply_point = get_object_or_404(SupplyPoint, id=supply_point_id)
    return supply_point_update(supply_point, payload, request.user)


@router.patch("/{supply_point_id}", response=BasicSupplyPointResponse)
def supply_point_update_partial_endpoint(request, supply_point_id: int, payload: SupplyPointUpdateRequest):
    supply_point = get_object_or_404(SupplyPoint, id=supply_point_id)
    return supply_point_update(supply_point, payload, request.user)


@router.get("/{supply_point_id}", response=BasicSupplyPointResponse)
def supply_point_detail_endpoint(request, supply_point_id: int):
    supply_point = get_object_or_404(SupplyPoint, id=supply_point_id)
    return supply_point_detail(supply_point, request.user)


@router.post("/delete/")
def delete_supply_point_endpoint(request, payload: DeleteRequest):
    delete_supply_points(payload, request.user)


@router.post("/export/csv/")
def supply_point_export_endpoint(request):
    return FileResponse(
        generate_csv_file("supply_point", supply_point_export_headers, SupplyPoint.objects.all())
    )
