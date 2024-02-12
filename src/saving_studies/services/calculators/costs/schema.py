from ninja import Schema
from pydantic import condecimal

from rates.choices import PriceTypes


class CostCalculatorInfo(Schema):
    id: int | None
    name: str | None
    energy_price_1: condecimal(decimal_places=6, ge=0) | None
    energy_price_2: condecimal(decimal_places=6, ge=0) | None
    energy_price_3: condecimal(decimal_places=6, ge=0) | None
    energy_price_4: condecimal(decimal_places=6, ge=0) | None
    energy_price_5: condecimal(decimal_places=6, ge=0) | None
    energy_price_6: condecimal(decimal_places=6, ge=0) | None
    consumption_p1: condecimal(decimal_places=2, ge=0) | None
    consumption_p2: condecimal(decimal_places=2, ge=0) | None
    consumption_p3: condecimal(decimal_places=2, ge=0) | None
    consumption_p4: condecimal(decimal_places=2, ge=0) | None
    consumption_p5: condecimal(decimal_places=2, ge=0) | None
    consumption_p6: condecimal(decimal_places=2, ge=0) | None
    power_1: condecimal(decimal_places=2, ge=0) | None
    power_2: condecimal(decimal_places=2, ge=0) | None
    power_3: condecimal(decimal_places=2, ge=0) | None
    power_4: condecimal(decimal_places=2, ge=0) | None
    power_5: condecimal(decimal_places=2, ge=0) | None
    power_6: condecimal(decimal_places=2, ge=0) | None
    power_price_1: condecimal(decimal_places=6, ge=0) | None
    power_price_2: condecimal(decimal_places=6, ge=0) | None
    power_price_3: condecimal(decimal_places=6, ge=0) | None
    power_price_4: condecimal(decimal_places=6, ge=0) | None
    power_price_5: condecimal(decimal_places=6, ge=0) | None
    power_price_6: condecimal(decimal_places=6, ge=0) | None
    price_type: str = PriceTypes.FIXED
    fixed_term_price: condecimal(decimal_places=6, ge=0) | None

    class Config:
        orm_mode = True
