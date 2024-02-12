from moneyed import Money
from ninja import Schema


class SuggestedRateCosts(Schema):
    final_cost: Money | None
    total_cost: Money | None
    energy_cost: Money | None
    power_cost: Money | None
    fixed_cost: Money | None
    other_costs: Money | None
    ie_cost: Money | None
    ih_cost: Money | None
    iva_cost: Money | None

    class Config:
        arbitrary_types_allowed = True
