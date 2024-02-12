from ninja import ModelSchema

from saving_studies.models import SavingStudy


class BasicSavingStudyResponse(ModelSchema):
    class Config:
        model = SavingStudy
        model_fields = [
            "id",
            "cups",
        ]


class SavingStudyListResponse(ModelSchema):
    class Config:
        model = SavingStudy
        model_fields = [
            "id",
            "cups",
        ]


class SavingStudyDetailResponse(ModelSchema):
    class Config:
        model = SavingStudy
        model_fields = [
            "id",
            "energy_type",
            "is_existing_client",
            "is_from_sips",
            "is_compare_conditions",
            "cups",
            "analyzed_days",
            "current_marketer",
            "current_rate_type",
            "client_type",
            "client_name",
            "client_nif",
            "consumption_p1",
            "consumption_p2",
            "consumption_p3",
            "consumption_p4",
            "consumption_p5",
            "consumption_p6",
            "annual_consumption",
            "energy_price_1",
            "energy_price_2",
            "energy_price_3",
            "energy_price_4",
            "energy_price_5",
            "energy_price_6",
            "power_1",
            "power_2",
            "power_3",
            "power_4",
            "power_5",
            "power_6",
            "power_price_1",
            "power_price_2",
            "power_price_3",
            "power_price_4",
            "power_price_5",
            "power_price_6",
            "fixed_price",
            "other_cost_kwh",
            "other_cost_percentage",
            "other_cost_eur_month",
            # "suggested_rates",
            # "contract",
        ]
