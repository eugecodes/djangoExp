from typing import List

from django.http import FileResponse
from django.shortcuts import get_object_or_404
from ninja import Router, Query
from ninja.pagination import paginate

from common.api.requests import DeleteRequest
from common.export import generate_csv_file
from common.pagination import CustomPagination
from commissions.api.schemas.exports import commission_export_headers
from commissions.api.schemas.requests import CommissionRequest, CommissionUpdateRequest
from commissions.api.schemas.filters import CommissionFilterSchema
from commissions.api.schemas.responses import (
    CommissionListResponse,
    BasicCommissionResponse,
)
from commissions.services import (
    commission_create,
    commission_update,
    delete_commissions,
    commission_list,
    commission_detail,
)
from commissions.models import Commission

router = Router()


@router.get("", response=List[CommissionListResponse])
@paginate(CustomPagination)
def commission_list_endpoint(request, filters: CommissionFilterSchema = Query(...)):
    return commission_list(filters, request.user)


@router.post("", response={201: BasicCommissionResponse})
def commission_create_endpoint(request, payload: CommissionRequest):
    return commission_create(payload, request.user)


@router.put("/{commission_id}", response=BasicCommissionResponse)
def commission_update_endpoint(request, commission_id: int, payload: CommissionUpdateRequest):
    commission = get_object_or_404(Commission, id=commission_id)
    return commission_update(commission, payload, request.user)


@router.patch("/{commission_id}", response=BasicCommissionResponse)
def commission_update_partial_endpoint(request, commission_id: int, payload: CommissionUpdateRequest):
    commission = get_object_or_404(Commission, id=commission_id)
    return commission_update(commission, payload, request.user)


@router.get("/{commission_id}", response=BasicCommissionResponse)
def commission_detail_endpoint(request, commission_id: int):
    commission = get_object_or_404(Commission, id=commission_id)
    return commission_detail(commission, request.user)


@router.post("/delete/")
def delete_commission_endpoint(request, payload: DeleteRequest):
    delete_commissions(payload, request.user)


@router.post("/export/csv/")
def commission_export_endpoint(request):
    return FileResponse(
        generate_csv_file("commission", commission_export_headers, Commission.objects.all())
    )
