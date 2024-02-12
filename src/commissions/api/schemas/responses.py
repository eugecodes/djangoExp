from ninja import ModelSchema

from commissions.models import Commission


class BasicCommissionResponse(ModelSchema):
    class Config:
        model = Commission
        model_fields = ["id", "name"]


class CommissionListResponse(ModelSchema):
    class Config:
        model = Commission
        model_fields = ["id", "name"]


class CommissionDetailResponse(ModelSchema):
    class Config:
        model = Commission
        model_fields = [
            "id",
            "name",
            "percentage_test_commission",
            "range_type",
            "rate_type_segmentation",
            "min_consumption",
            "max_consumption",
            "min_power",
            "max_power",
            "test_commission",
        ]
