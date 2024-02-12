from ninja import ModelSchema

from channels.models import Channel


class BasicChannelResponse(ModelSchema):
    class Config:
        model = Channel
        model_fields = ["id", "created"]


class ChannelListResponse(ModelSchema):
    class Config:
        model = Channel
        model_fields = ["id", "created"]


class ChannelDetailResponse(ModelSchema):
    class Config:
        model = Channel
        model_fields = ["id", "created"]
