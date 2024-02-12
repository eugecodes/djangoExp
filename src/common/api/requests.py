from ninja import Schema


class DeleteRequest(Schema):
    ids: list[int]
