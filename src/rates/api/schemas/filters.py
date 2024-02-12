from datetime import datetime
from typing import Optional

from ninja import FilterSchema
from pydantic import Field


class RateFilterSchema(FilterSchema):
    name: Optional[str] = Field(None, q="name__icontains")
    created_after: Optional[datetime] = Field(None, q="created__gte")
