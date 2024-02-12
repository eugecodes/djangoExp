from typing import List

from django.http import FileResponse
from django.shortcuts import get_object_or_404
from ninja import Router, Query
from ninja.pagination import paginate

from common.api.requests import DeleteRequest
from common.export import generate_csv_file
from common.pagination import CustomPagination
from contracts.api.schemas.exports import contract_export_headers
from contracts.api.schemas.requests import ContractRequest, ContractUpdateRequest
from contracts.api.schemas.filters import ContractFilterSchema
from contracts.api.schemas.responses import (
    ContractListResponse,
    BasicContractResponse,
)
from contracts.services import (
    contract_create,
    contract_update,
    delete_contracts,
    contract_list,
    contract_detail,
)
from contracts.models import Contract

router = Router()


@router.get("", response=List[ContractListResponse])
@paginate(CustomPagination)
def contract_list_endpoint(request, filters: ContractFilterSchema = Query(...)):
    return contract_list(filters, request.user)


@router.post("", response={201: BasicContractResponse})
def contract_create_endpoint(request, payload: ContractRequest):
    return contract_create(payload, request.user)


@router.put("/{contract_id}", response=BasicContractResponse)
def contract_update_endpoint(request, contract_id: int, payload: ContractUpdateRequest):
    contract = get_object_or_404(Contract, id=contract_id)
    return contract_update(contract, payload, request.user)


@router.patch("/{contract_id}", response=BasicContractResponse)
def contract_update_partial_endpoint(request, contract_id: int, payload: ContractUpdateRequest):
    contract = get_object_or_404(Contract, id=contract_id)
    return contract_update(contract, payload, request.user)


@router.get("/{contract_id}", response=BasicContractResponse)
def contract_detail_endpoint(request, contract_id: int):
    contract = get_object_or_404(Contract, id=contract_id)
    return contract_detail(contract, request.user)


@router.post("/delete/")
def delete_contract_endpoint(request, payload: DeleteRequest):
    delete_contracts(payload, request.user)


@router.post("/export/csv/")
def contract_export_endpoint(request):
    return FileResponse(
        generate_csv_file("contract", contract_export_headers, Contract.objects.all())
    )
