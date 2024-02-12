from typing import List

from django.contrib.auth import get_user_model
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from ninja import Router, Query
from ninja.pagination import paginate

from common.api.requests import DeleteRequest
from common.export import generate_csv_file
from common.pagination import CustomPagination
from users.api.schemas.exports import user_export_headers
from users.api.schemas.filters import UserFilterSchema
from users.api.schemas.requests import UserLoginRequest, UserRequest
from users.api.schemas.responses import (
    UserLoginResponse,
    UserMeDetailResponse,
    UserListResponse,
    BasicUserResponse,
)
from users.services.login import login_user, logout_user
from users.services.user import (
    user_create,
    user_update,
    delete_users,
    user_list,
    user_detail,
)

User = get_user_model()

router = Router()


@router.post("/login", response=UserLoginResponse, auth=None)
def login(request, data: UserLoginRequest):
    return login_user(data)


@router.post("/logout")
def user_logout_endpoint(request):
    logout_user(request.user)


@router.get("/me", response=UserMeDetailResponse)
def user_me_endpoint(request):
    return request.user


# @router.post("/forgot-password")
# def user_forgot_password_endpoint(requests, user_email: ForgotPasswordRequest):
#     background_tasks.add_task(forgot_password, user_email)
#
#
# @router.post(
#     "/reset-password", status_code=status.HTTP_204_NO_CONTENT, responses={**RESPONSES}
# )
# def user_reset_password_endpoint(
#     reset_password_request: schemas.ResetPasswordRequest,
#     db: Session = Depends(get_db),
# ):
#     reset_password(db, reset_password_request)
#
#

#
#

#
#
# @router.post(
#     "/change-password", status_code=status.HTTP_204_NO_CONTENT, responses={**RESPONSES}
# )
# def user_change_password_endpoint(
#     change_password_request: schemas.ChangePasswordRequest,
#     current_user: User = Depends(get_current_user),
#     db: Session = Depends(get_db),
# ):
#     change_password(
#         db,
#         current_user,
#         change_password_request.old_password,
#         change_password_request.new_password,
#     )
#


@router.get("", response=List[UserListResponse])
@paginate(CustomPagination)
def user_list_endpoint(request, filters: UserFilterSchema = Query(...)):
    return user_list(filters, request.user)


@router.post("", response=BasicUserResponse)
def user_create_endpoint(request, payload: UserRequest):
    return user_create(payload, request.user)


@router.put("/{user_id}", response=BasicUserResponse)
def user_update_endpoint(request, user_id: int, payload: UserRequest):
    user = get_object_or_404(User, id=user_id)
    return user_update(user, payload, request.user)


@router.patch("/{user_id}", response=BasicUserResponse)
def user_update_partial_endpoint(request, user_id: int, payload: UserRequest):
    user = get_object_or_404(User, id=user_id)
    return user_update(user, payload, request.user)


@router.get("/{user_id}", response=BasicUserResponse)
def user_detail_endpoint(request, user_id: int):
    user = get_object_or_404(User, id=user_id)
    return user_detail(user, request.user)


@router.post("/delete/")
def delete_users_endpoint(request, payload: DeleteRequest):
    delete_users(payload)


@router.post("/export/csv/")
def user_export_endpoint(request):
    return FileResponse(
        generate_csv_file("users", user_export_headers, User.objects.all())
    )


# @router.post(
#     "/export/csv",
#     status_code=status.HTTP_200_OK,
#     response_class=FileResponse,
#     dependencies=[Depends(get_current_user)],
#     responses={**RESPONSES},
# )
# def user_export_endpoint(
#     user_filter: schemas.UserFilter = FilterDepends(
#         schemas.UserFilter, use_cache=False
#     ),
#     current_user: User = Depends(get_current_user),
#     db: Session = Depends(get_db),
# ) -> FileResponse:
#     return FileResponse(
#         generate_csv_file(
#             "users",
#             schemas.user_export_headers,
#             list_users(db, user_filter, current_user).all(),
#         )
#     )
