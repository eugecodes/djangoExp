from ninja import ModelSchema

from commissions.models import Commission


class CommissionRequest(ModelSchema):
    rate_type_id: int

    class Config:
        model = Commission
        model_fields = [
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
        optional_fields = [
            "percentage_test_commission",
            "range_type",
            "rate_type_segmentation",
            "min_consumption",
            "max_consumption",
            "min_power",
            "max_power",
            "test_commission",
        ]


class CommissionUpdateRequest(ModelSchema):
    class Config:
        model = Commission
        model_fields = [
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
        optional_fields = [
            "percentage_test_commission",
            "range_type",
            "rate_type_segmentation",
            "min_consumption",
            "max_consumption",
            "min_power",
            "max_power",
            "test_commission",
        ]
