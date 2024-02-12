from typing import List

from django.http import FileResponse
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.pagination import paginate

from common.api.requests import DeleteRequest
from common.export import generate_csv_file
from common.pagination import CustomPagination
from roles.api.schemas.exports import role_export_headers
from roles.api.schemas.requests import RoleRequest
from roles.api.schemas.responses import (
    RoleListResponse,
    BasicRoleResponse,
)
from roles.models import Role
from roles.services import (
    role_create,
    role_update,
    delete_roles,
    roles_list,
    role_detail,
)

router = Router()


@router.get("", response=List[RoleListResponse])
@paginate(CustomPagination)
def role_list_endpoint(request):
    return roles_list(request.user)


@router.post("", response=BasicRoleResponse)
def role_create_endpoint(request, payload: RoleRequest):
    return role_create(payload, request.user)


@router.put("/{role_id}", response=BasicRoleResponse)
def role_update_endpoint(request, role_id: int, payload: RoleRequest):
    role = get_object_or_404(Role, id=role_id)
    return role_update(role, payload, request.user)


@router.patch("/{role_id}", response=BasicRoleResponse)
def role_update_partial_endpoint(request, role_id: int, payload: RoleRequest):
    role = get_object_or_404(Role, id=role_id)
    return role_update(role, payload, request.user)


@router.get("/{role_id}", response=BasicRoleResponse)
def role_detail_endpoint(request, role_id: int):
    role = get_object_or_404(Role, id=role_id)
    return role_detail(role, request.user)


@router.post("/delete/")
def delete_role_endpoint(request, payload: DeleteRequest):
    delete_roles(payload, request.user)


@router.post("/export/csv/")
def role_export_endpoint(request):
    return FileResponse(
        generate_csv_file("role", role_export_headers, Role.objects.all())
    )
