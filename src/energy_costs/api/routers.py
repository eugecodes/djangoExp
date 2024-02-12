from typing import List

from django.http import FileResponse
from django.shortcuts import get_object_or_404
from ninja import Router, Query
from ninja.pagination import paginate

from common.api.requests import DeleteRequest
from common.export import generate_csv_file
from common.pagination import CustomPagination
from energy_costs.api.schemas.exports import energy_cost_export_headers
from energy_costs.api.schemas.requests import EnergyCostRequest, EnergyCostUpdateRequest
from energy_costs.api.schemas.filters import EnergyCostFilterSchema
from energy_costs.api.schemas.responses import (
    EnergyCostListResponse,
    BasicEnergyCostResponse,
)
from energy_costs.services import (
    energy_cost_create,
    energy_cost_update,
    delete_energy_costs,
    energy_cost_list,
    energy_cost_detail,
)
from energy_costs.models import EnergyCost

router = Router()


@router.get("", response=List[EnergyCostListResponse])
@paginate(CustomPagination)
def energy_cost_list_endpoint(request, filters: EnergyCostFilterSchema = Query(...)):
    return energy_cost_list(filters, request.user)


@router.post("", response={201: BasicEnergyCostResponse})
def energy_cost_create_endpoint(request, payload: EnergyCostRequest):
    return energy_cost_create(payload, request.user)


@router.put("/{energy_cost_id}", response=BasicEnergyCostResponse)
def energy_cost_update_endpoint(request, energy_cost_id: int, payload: EnergyCostUpdateRequest):
    energy_cost = get_object_or_404(EnergyCost, id=energy_cost_id)
    return energy_cost_update(energy_cost, payload, request.user)


@router.patch("/{energy_cost_id}", response=BasicEnergyCostResponse)
def energy_cost_update_partial_endpoint(request, energy_cost_id: int, payload: EnergyCostUpdateRequest):
    energy_cost = get_object_or_404(EnergyCost, id=energy_cost_id)
    return energy_cost_update(energy_cost, payload, request.user)


@router.get("/{energy_cost_id}", response=BasicEnergyCostResponse)
def energy_cost_detail_endpoint(request, energy_cost_id: int):
    energy_cost = get_object_or_404(EnergyCost, id=energy_cost_id)
    return energy_cost_detail(energy_cost, request.user)


@router.post("/delete/")
def delete_energy_cost_endpoint(request, payload: DeleteRequest):
    delete_energy_costs(payload, request.user)


@router.post("/export/csv/")
def energy_cost_export_endpoint(request):
    return FileResponse(
        generate_csv_file("energy_cost", energy_cost_export_headers, EnergyCost.objects.all())
    )
