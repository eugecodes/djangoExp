from ninja import ModelSchema

from channels.models import Channel


class ChannelRequest(ModelSchema):
    class Config:
        model = Channel
        model_fields = [
            "name",
        ]
