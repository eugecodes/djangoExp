from typing import List

from django.http import FileResponse
from django.shortcuts import get_object_or_404
from ninja import Router, Query
from ninja.pagination import paginate

from channels.api.schemas.exports import channel_export_headers
from channels.api.schemas.filters import ChannelFilterSchema
from channels.api.schemas.requests import ChannelRequest
from channels.api.schemas.responses import (
    ChannelListResponse,
    BasicChannelResponse,
)
from channels.models import Channel
from channels.services import (
    channel_create,
    channel_update,
    delete_channels,
    channel_list,
    channel_detail,
)
from common.api.requests import DeleteRequest
from common.export import generate_csv_file
from common.pagination import CustomPagination

router = Router()


@router.get("", response=List[ChannelListResponse])
@paginate(CustomPagination)
def channel_list_endpoint(request, filters: ChannelFilterSchema = Query(...)):
    return channel_list(filters, request.user)


@router.post("", response=BasicChannelResponse)
def channel_create_endpoint(request, payload: ChannelRequest):
    return channel_create(payload, request.channel)


@router.put("/{channel_id}", response=BasicChannelResponse)
def channel_update_endpoint(request, channel_id: int, payload: ChannelRequest):
    channel = get_object_or_404(Channel, id=channel_id)
    return channel_update(channel, payload, request.channel)


@router.patch("/{channel_id}", response=BasicChannelResponse)
def channel_update_partial_endpoint(request, channel_id: int, payload: ChannelRequest):
    channel = get_object_or_404(Channel, id=channel_id)
    return channel_update(channel, payload, request.channel)


@router.get("/{channel_id}", response=BasicChannelResponse)
def channel_detail_endpoint(request, channel_id: int):
    channel = get_object_or_404(Channel, id=channel_id)
    return channel_detail(channel, request.user)


@router.post("/delete/")
def delete_channel_endpoint(request, payload: DeleteRequest):
    delete_channels(payload, request.admin_user)


@router.post("/export/csv/")
def channel_export_endpoint(request):
    return FileResponse(
        generate_csv_file("channel", channel_export_headers, Channel.objects.all())
    )
