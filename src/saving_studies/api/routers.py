from typing import List

from django.http import FileResponse
from django.shortcuts import get_object_or_404
from ninja import Router, Query
from ninja.pagination import paginate

from common.api.requests import DeleteRequest
from common.export import generate_csv_file
from common.pagination import CustomPagination
from saving_studies.api.schemas.exports import saving_study_export_headers
from saving_studies.api.schemas.filters import SavingStudyFilterSchema
from saving_studies.api.schemas.requests import (
    SavingStudyRequest,
    SavingStudyUpdateRequest,
)
from saving_studies.api.schemas.responses import (
    SavingStudyListResponse,
    BasicSavingStudyResponse,
)
from saving_studies.models import SavingStudy
from saving_studies.services.base import (
    saving_study_create,
    saving_study_update,
    delete_saving_studies,
    saving_study_list,
    saving_study_detail,
)

router = Router()


@router.get("", response=List[SavingStudyListResponse])
@paginate(CustomPagination)
def saving_study_list_endpoint(request, filters: SavingStudyFilterSchema = Query(...)):
    return saving_study_list(filters, request.user)


@router.post("", response={201: BasicSavingStudyResponse})
def saving_study_create_endpoint(request, payload: SavingStudyRequest):
    return saving_study_create(payload, request.user)


@router.put("/{saving_study_id}", response=BasicSavingStudyResponse)
def saving_study_update_endpoint(
    request, saving_study_id: int, payload: SavingStudyUpdateRequest
):
    saving_study = get_object_or_404(SavingStudy, id=saving_study_id)
    return saving_study_update(saving_study, payload, request.user)


@router.patch("/{saving_study_id}", response=BasicSavingStudyResponse)
def saving_study_update_partial_endpoint(
    request, saving_study_id: int, payload: SavingStudyUpdateRequest
):
    saving_study = get_object_or_404(SavingStudy, id=saving_study_id)
    return saving_study_update(saving_study, payload, request.user)


@router.get("/{saving_study_id}", response=BasicSavingStudyResponse)
def saving_study_detail_endpoint(request, saving_study_id: int):
    saving_study = get_object_or_404(SavingStudy, id=saving_study_id)
    return saving_study_detail(saving_study, request.user)


@router.post("/delete/")
def delete_saving_study_endpoint(request, payload: DeleteRequest):
    delete_saving_studies(payload, request.user)


@router.post("/export/csv/")
def saving_study_export_endpoint(request):
    return FileResponse(
        generate_csv_file(
            "saving_study", saving_study_export_headers, SavingStudy.objects.all()
        )
    )
