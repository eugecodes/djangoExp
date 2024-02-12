from typing import List, Any

from ninja import Schema
from ninja.pagination import PaginationBase

EMPTY_LIST_RESPONSE = {"items": [], "total": 0, "page": 1, "size": 10, "pages": 1}


class CustomPagination(PaginationBase):
    class Input(Schema):
        size: int = 10
        page: int = 1

    class Output(Schema):
        items: List[Any]  # `items` is a default attribute
        total: int
        page: int
        size: int
        pages: int

    def paginate_queryset(self, queryset, pagination: Input, **params):
        size = pagination.size
        page = pagination.page
        first_item = size * (page - 1)
        last_item = first_item + size
        total = queryset.count()
        total_pages = max(total // size, 1)
        return {
            "items": queryset[first_item:last_item],
            "total": total,
            "page": page,
            "size": size,
            "pages": total_pages,
        }
