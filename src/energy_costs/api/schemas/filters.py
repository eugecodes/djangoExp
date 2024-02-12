from datetime import datetime
from typing import Optional

from ninja import FilterSchema
from pydantic import Field


class EnergyCostFilterSchema(FilterSchema):
    code: Optional[str] = Field(None, q="code__icontains")
    created_after: Optional[datetime] = Field(None, q="created__gte")
