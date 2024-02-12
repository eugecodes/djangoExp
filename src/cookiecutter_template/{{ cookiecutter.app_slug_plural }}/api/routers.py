from typing import List

from django.http import FileResponse
from django.shortcuts import get_object_or_404
from ninja import Router, Query
from ninja.pagination import paginate

from common.api.requests import DeleteRequest
from common.export import generate_csv_file
from common.pagination import CustomPagination
from {{ cookiecutter.app_slug_plural }}.api.schemas.exports import {{ cookiecutter.app_slug }}_export_headers
from {{ cookiecutter.app_slug_plural }}.api.schemas.requests import {{ cookiecutter.app_name }}Request, {{ cookiecutter.app_name }}UpdateRequest
from {{ cookiecutter.app_slug_plural }}.api.schemas.filters import {{ cookiecutter.app_name }}FilterSchema
from {{ cookiecutter.app_slug_plural }}.api.schemas.responses import (
    {{ cookiecutter.app_name }}ListResponse,
    Basic{{ cookiecutter.app_name }}Response,
)
from {{ cookiecutter.app_slug_plural }}.services import (
    {{ cookiecutter.app_slug }}_create,
    {{ cookiecutter.app_slug }}_update,
    delete_{{ cookiecutter.app_slug_plural }},
    {{ cookiecutter.app_slug }}_list,
    {{ cookiecutter.app_slug }}_detail,
)
from {{ cookiecutter.app_slug_plural }}.models import {{ cookiecutter.app_name }}

router = Router()


@router.get("", response=List[{{ cookiecutter.app_name }}ListResponse])
@paginate(CustomPagination)
def {{ cookiecutter.app_slug }}_list_endpoint(request, filters: {{ cookiecutter.app_name }}FilterSchema = Query(...)):
    return {{ cookiecutter.app_slug }}_list(filters, request.user)


@router.post("", response={201: Basic{{ cookiecutter.app_name }}Response})
def {{ cookiecutter.app_slug }}_create_endpoint(request, payload: {{ cookiecutter.app_name }}Request):
    return {{ cookiecutter.app_slug }}_create(payload, request.user)


@router.put("/{{'{'}}{{ cookiecutter.app_slug }}_id{{'}'}}", response=Basic{{ cookiecutter.app_name }}Response)
def {{ cookiecutter.app_slug }}_update_endpoint(request, {{ cookiecutter.app_slug }}_id: int, payload: {{ cookiecutter.app_name }}UpdateRequest):
    {{ cookiecutter.app_slug }} = get_object_or_404({{ cookiecutter.app_name }}, id={{ cookiecutter.app_slug }}_id)
    return {{ cookiecutter.app_slug }}_update({{ cookiecutter.app_slug }}, payload, request.user)


@router.patch("/{{'{'}}{{ cookiecutter.app_slug }}_id{{'}'}}", response=Basic{{ cookiecutter.app_name }}Response)
def {{ cookiecutter.app_slug }}_update_partial_endpoint(request, {{ cookiecutter.app_slug }}_id: int, payload: {{ cookiecutter.app_name }}UpdateRequest):
    {{ cookiecutter.app_slug }} = get_object_or_404({{ cookiecutter.app_name }}, id={{ cookiecutter.app_slug }}_id)
    return {{ cookiecutter.app_slug }}_update({{ cookiecutter.app_slug }}, payload, request.user)


@router.get("/{{'{'}}{{ cookiecutter.app_slug }}_id{{'}'}}", response=Basic{{ cookiecutter.app_name }}Response)
def {{ cookiecutter.app_slug }}_detail_endpoint(request, {{ cookiecutter.app_slug }}_id: int):
    {{ cookiecutter.app_slug }} = get_object_or_404({{ cookiecutter.app_name }}, id={{ cookiecutter.app_slug }}_id)
    return {{ cookiecutter.app_slug }}_detail({{ cookiecutter.app_slug }}, request.user)


@router.post("/delete/")
def delete_{{ cookiecutter.app_slug }}_endpoint(request, payload: DeleteRequest):
    delete_{{ cookiecutter.app_slug_plural }}(payload, request.user)


@router.post("/export/csv/")
def {{ cookiecutter.app_slug }}_export_endpoint(request):
    return FileResponse(
        generate_csv_file("{{ cookiecutter.app_slug }}", {{ cookiecutter.app_slug }}_export_headers, {{ cookiecutter.app_name }}.objects.all())
    )
