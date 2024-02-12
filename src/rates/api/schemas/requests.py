from ninja import ModelSchema

from rates.models import Rate


class RateRequest(ModelSchema):
    marketer_id: int
    rate_type_id: int

    class Config:
        model = Rate
        model_fields = [
            "name",
            "energy_type",
            "price_type",
            "client_types",
            "max_power",
            "min_power",
            "min_consumption",
            "max_consumption",
            "energy_price_1",
            "energy_price_2",
            "energy_price_3",
            "energy_price_4",
            "energy_price_5",
            "energy_price_6",
            "power_price_1",
            "power_price_2",
            "power_price_3",
            "power_price_4",
            "power_price_5",
            "power_price_6",
            "fixed_term_price",
            "permanency",
            "length",
            "is_full_renewable",
            "compensation_surplus",
            "compensation_surplus_value",
        ]
        fields_optional = [
            "max_power",
            "min_power",
            "min_consumption",
            "max_consumption",
            "energy_price_1",
            "energy_price_2",
            "energy_price_3",
            "energy_price_4",
            "energy_price_5",
            "energy_price_6",
            "power_price_1",
            "power_price_2",
            "power_price_3",
            "power_price_4",
            "power_price_5",
            "power_price_6",
            "fixed_term_price",
            "is_full_renewable",
            "compensation_surplus",
            "compensation_surplus_value",
        ]


class RateUpdateRequest(ModelSchema):
    rate_type_id: int

    class Config:
        model = Rate
        model_fields = [
            "created",
            "name",
            "energy_type",
            "price_type",
            "client_types",
            "max_power",
            "min_power",
            "min_consumption",
            "max_consumption",
            "energy_price_1",
            "energy_price_2",
            "energy_price_3",
            "energy_price_4",
            "energy_price_5",
            "energy_price_6",
            "power_price_1",
            "power_price_2",
            "power_price_3",
            "power_price_4",
            "power_price_5",
            "power_price_6",
            "fixed_term_price",
            "permanency",
            "length",
            "is_full_renewable",
            "compensation_surplus",
            "compensation_surplus_value",
        ]
        fields_optional = [
            "client_types",
            "max_power",
            "min_power",
            "min_consumption",
            "max_consumption",
            "energy_price_1",
            "energy_price_2",
            "energy_price_3",
            "energy_price_4",
            "energy_price_5",
            "energy_price_6",
            "power_price_1",
            "power_price_2",
            "power_price_3",
            "power_price_4",
            "power_price_5",
            "power_price_6",
            "fixed_term_price",
            "is_full_renewable",
            "compensation_surplus",
            "compensation_surplus_value",
            "rate_type_id",
        ]
