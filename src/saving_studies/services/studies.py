import logging
from decimal import Decimal
from typing import List, Tuple

from django.db.models import Q
from django.db.models.functions import Coalesce

from common.choices import EnergyTypes
from marketers.choices import MarketerStatus
from rate_types.choices import RateTypeStatus
from rates.choices import PriceTypes
from rates.models import Rate
from saving_studies.models import SavingStudy
from suggested_rates.models import SuggestedRate
from suggested_rates.services.generator import SuggestedRatesGenerator

logger = logging.getLogger(__name__)

DAYS_PER_MONTH = Decimal("30.4167")
OTHER_COST_FIELDS = {
    "eur/month": "other_cost_kwh",
    "percentage": "other_cost_percentage",
    "eur/kwh": "other_cost_eur_month",
}
IVA = "iva"
IVA_REDUCIDO = "iva_reducido"
IMP_HIDROCARBUROS = "imp_hidrocarburos"
IMP_ELECTRICOS = "imp_electricos"


def get_candidate_rates(saving_study: SavingStudy):
    power_min_required = saving_study.power_6 or saving_study.power_2 or 0
    rates = Rate.objects.filter(
        status=Rate.ENABLED,
        rate_type__status=RateTypeStatus.ENABLED,
        marketer__status=MarketerStatus.ENABLED,
        rate_type_id=saving_study.current_rate_type_id,
        client_types__icontains=saving_study.client_type,
    )

    rates = rates.annotate(
        minimun_power=Coalesce("min_power", Decimal(0)),
        maximun_power=Coalesce("max_power", Decimal(99999999)),
    )

    rates = rates.filter(
        Q(
            Q(rate_type__energy_type=EnergyTypes.ELECTRICITY)
            & Q(minimun_power__lte=Decimal(power_min_required))
            & Q(maximun_power__gte=Decimal(power_min_required))
            & Q(price_type=PriceTypes.FIXED)
        )
        | Q(
            Q(rate_type__energy_type=EnergyTypes.ELECTRICITY)
            & Q(price_type=PriceTypes.FIXED)
        )
        | Q(
            Q(rate_type__energy_type=EnergyTypes.GAS)
            & Q(min_consumption__lte=saving_study.annual_consumption)
            & Q(max_consumption__gte=saving_study.annual_consumption)
        )
    )

    return rates


def generate_suggested_rates_for_study(saving_study_id: int) -> List[SuggestedRate]:
    saving_study = SavingStudy.objects.get(id=saving_study_id)
    validate_saving_study_before_generating_rates(saving_study)

    logger.info(f"[saving_study_id={saving_study_id}] Generating suggested rates")
    suggested_rates_deleted = saving_study.suggested_rates.values_list("id", flat=True)
    saving_study.suggested_rates.delete()
    logger.info(
        f"[saving_study_id={saving_study_id}] {suggested_rates_deleted} Suggested rates deleted"
    )
    candidate_rates = get_candidate_rates(saving_study)
    logger.info(
        f"[saving_study_id={saving_study_id}] %s Candidate rates found",
        candidate_rates.count(),
    )

    suggested_rates_generator = SuggestedRatesGenerator(saving_study)
    suggested_rates = suggested_rates_generator.generate_suggested_rates(
        candidate_rates
    )

    logger.info(
        f"[saving_study_id={saving_study.id}] {len(suggested_rates)} Suggested rates saved"
    )
    return suggested_rates


#
# def saving_study_create(
#     db: Session, saving_study_request: SavingStudyRequest, current_user: User
# ) -> SavingStudy:
#     saving_study = SavingStudy(**saving_study_request.dict())
#     saving_study.user_creator_id = current_user.id
#
#     if saving_study_request.current_rate_type_id:
#         current_rate_type = get_rate_type(db, saving_study_request.current_rate_type_id)
#         saving_study.current_rate_type_id = current_rate_type.id
#
#     if (
#         saving_study_request.is_from_sips
#         and saving_study.energy_type == EnergyType.electricity
#     ):
#         saving_study = fill_study_with_sips(saving_study)
#
#     try:
#         saving_study = create_saving_study_db(db, saving_study)
#     except IntegrityError:
#         db.rollback()
#         raise HTTPException(
#             status.HTTP_409_CONFLICT, detail="value_error.already_exists"
#         )
#     return saving_study
#
#
# def list_saving_studies(db: Session, saving_study_filter: SavingStudyFilter):
#     return saving_study_filter.sort(
#         saving_study_filter.filter(
#             get_saving_studies_queryset(db, None, SavingStudy.is_deleted == false())
#         )
#     )
#
#

#
#
# def saving_study_update(
#     db: Session,
#     saving_study_id: int,
#     saving_study_data: SavingStudyRequest,
# ) -> SavingStudy:
#     saving_study_dict = saving_study_data.dict(exclude_unset=True)
#
#     saving_study = SavingStudy.objects.get(id=saving_study_id)
#     rate_type_id = saving_study_dict.get("current_rate_type_id")
#     if not rate_type_id:
#         _ = (
#             get_rate_type(db, saving_study.current_rate_type_id)
#             if saving_study.current_rate_type_id
#             else None
#         )
#     else:
#         _ = get_rate_type(db, rate_type_id)
#
#     update_from_dict(saving_study, saving_study_dict)
#     saving_study = update_obj_db(db, saving_study)
#     return saving_study


def validate_saving_study_before_generating_rates(saving_study: SavingStudy) -> None:
    if not saving_study.current_rate_type_id:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="value_error.current_rate_type_id.missing",
        )

    if saving_study.energy_type == EnergyType.electricity:
        if not saving_study.power_1:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="value_error.power_1.missing",
            )
        elif not saving_study.power_2:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="value_error.power_2.missing",
            )

    if saving_study.is_compare_conditions and not saving_study.energy_price_1:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="value_error.energy_price_1.missing",
        )


def finish_saving_study(
    saving_study_id: int, suggested_rate_id: int
) -> Tuple[SavingStudy, SuggestedRate]:
    saving_study = SavingStudy.objects.get(id=saving_study_id)
    suggested_rate = get_suggested_rate(suggested_rate_id, saving_study_id)
    saving_study, suggested_rate = finish_study_db(saving_study, suggested_rate)
    return saving_study, suggested_rate


def suggested_rate_update(
    saving_study_id: int,
    suggested_rate_id: int,
    suggested_rate_data: SuggestedRateUpdate,
) -> SuggestedRate:
    saving_study = SavingStudy.objects.get(id=saving_study_id)
    suggested_rate = get_suggested_rate(suggested_rate_id, saving_study_id)

    suggested_rate_dict = suggested_rate_data.dict(exclude_unset=True)
    validate_suggested_rate_for_update(suggested_rate, suggested_rate_dict)

    rate = get_rate_by(Rate.name == suggested_rate.rate_name)
    if not rate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="rate_not_exist"
        )
    suggested_rate_generator = SuggestedRatesGenerator(saving_study)
    (
        new_costs,
        theoretical_commission,
    ) = suggested_rate_generator.compute_final_cost_and_commission(
        rate, suggested_rate_dict["applied_profit_margin"]
    )
    suggested_rate.final_cost = new_costs.final_cost
    suggested_rate.energy_cost = new_costs.energy_cost
    suggested_rate.power_cost = new_costs.power_cost
    suggested_rate.fixed_cost = new_costs.fixed_cost
    suggested_rate.ie_cost = new_costs.ie_cost
    suggested_rate.ih_cost = new_costs.ih_cost
    suggested_rate.other_costs = new_costs.other_costs
    suggested_rate.iva_cost = new_costs.iva_cost

    suggested_rate.theoretical_commission = theoretical_commission
    suggested_rate.total_commission = (
        suggested_rate.other_costs_commission + theoretical_commission
        if suggested_rate.other_costs_commission
        else theoretical_commission
    )

    suggested_rate.applied_profit_margin = suggested_rate_dict["applied_profit_margin"]
    update_obj_db(suggested_rate)

    return suggested_rate


def validate_suggested_rate_for_update(
    suggested_rate: SuggestedRate, data_for_update: dict
) -> None:
    applied_profit_margin = data_for_update["applied_profit_margin"]
    if (
        applied_profit_margin < suggested_rate.min_profit_margin
        or applied_profit_margin > suggested_rate.max_profit_margin
    ):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="value_error.applied_profit_margin.value_error",
        )


def duplicate_saving_study(saving_study_id: int) -> SavingStudy:
    saving_study = SavingStudy.objects.get(saving_study_id)
    saving_study.id = None
    saving_study.status = SavingStudy.IN_PROGRESS
    saving_study.save()
    return saving_study
