from ninja import ModelSchema

from contracts.models import Contract


class ContractRequest(ModelSchema):
    channel_id: int = None
    client_id: int
    rate_id: int
    saving_study_id: int = None
    supply_point_id: int = None

    class Config:
        model = Contract
        model_fields = [
            "power_1",
            "power_2",
            "power_3",
            "power_4",
            "power_5",
            "power_6",
            "start_date",
            "end_date",
            "expected_end_date",
            "preferred_start_date",
            "period",
            "signature_first_name",
            "signature_last_name",
            "signature_dni",
            "signature_email",
            "signature_phone",
        ]
        optional_fields = [
            "power_1",
            "power_2",
            "power_3",
            "power_4",
            "power_5",
            "power_6",
            "start_date",
            "end_date",
            "expected_end_date",
            "preferred_start_date",
            "period",
            "signature_first_name",
            "signature_last_name",
            "signature_dni",
            "signature_email",
            "signature_phone",
        ]


class ContractUpdateRequest(ModelSchema):
    saving_study_id: int = None

    class Config:
        model = Contract
        model_fields = [
            "power_1",
            "power_2",
            "power_3",
            "power_4",
            "power_5",
            "power_6",
            "start_date",
            "end_date",
            "expected_end_date",
            "preferred_start_date",
            "period",
            "signature_first_name",
            "signature_last_name",
            "signature_dni",
            "signature_email",
            "signature_phone",
        ]
        optional_fields = [
            "power_1",
            "power_2",
            "power_3",
            "power_4",
            "power_5",
            "power_6",
            "start_date",
            "end_date",
            "expected_end_date",
            "preferred_start_date",
            "period",
            "signature_first_name",
            "signature_last_name",
            "signature_dni",
            "signature_email",
            "signature_phone",
        ]
