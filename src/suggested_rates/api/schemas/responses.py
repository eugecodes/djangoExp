from ninja import ModelSchema

from suggested_rates.models import SuggestedRate


class BasicSuggestedRateResponse(ModelSchema):
    class Config:
        model = SuggestedRate
        model_fields = [
            "id",
            "created",
            "is_selected",
            "saving_study",
            "marketer_name",
            "has_contractual_commitment",
            "duration",
            "rate_name",
            "is_full_renewable",
            "has_net_metering",
            "net_metering_value",
            "profit_margin_type",
            "min_profit_margin",
            "max_profit_margin",
            "applied_profit_margin",
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
            "price_type",
            "final_cost",
            "energy_cost",
            "power_cost",
            "fixed_cost",
            "other_costs",
            "ie_cost",
            "ih_cost",
            "iva_cost",
            "total_commission",
            "theoretical_commission",
            "other_costs_commission",
            "saving_relative",
            "saving_absolute",
        ]


class SuggestedRateListResponse(ModelSchema):
    class Config:
        model = SuggestedRate
        model_fields = [
            "id",
            "rate_name",
        ]


class SuggestedRateDetailResponse(ModelSchema):
    class Config:
        model = SuggestedRate
        model_fields = [
            "id",
            "created",
            "is_selected",
            "saving_study",
            "marketer_name",
            "has_contractual_commitment",
            "duration",
            "rate_name",
            "is_full_renewable",
            "has_net_metering",
            "net_metering_value",
            "profit_margin_type",
            "min_profit_margin",
            "max_profit_margin",
            "applied_profit_margin",
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
            "price_type",
            "final_cost",
            "energy_cost",
            "power_cost",
            "fixed_cost",
            "other_costs",
            "ie_cost",
            "ih_cost",
            "iva_cost",
            "total_commission",
            "theoretical_commission",
            "other_costs_commission",
            "saving_relative",
            "saving_absolute",
        ]
