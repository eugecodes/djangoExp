from decimal import Decimal

import pytest
from moneyed import Money

from common.choices import EnergyTypes
from config import settings
from margins.choices import MarginType
from margins.models import Margin
from rates.models import Rate
from suggested_rates.services.generator import SuggestedRatesGenerator


@pytest.mark.django_db
def test_init(saving_study):
    generator = SuggestedRatesGenerator(saving_study)
    assert generator.saving_study == saving_study


@pytest.mark.django_db
def test_get_default_margin_rate_only_one_rate_type(saving_study, margin):
    generator = SuggestedRatesGenerator(saving_study)
    margin.type = MarginType.RATE_TYPE
    margin.save()
    assert generator.get_default_margin_rate(rate=margin.rate) == margin


@pytest.mark.django_db
def test_get_default_margin_rate_consume_range_no_annual_consumption_return_none(
    saving_study, margin
):
    saving_study.annual_consumption = None
    generator = SuggestedRatesGenerator(saving_study)
    margin.type = MarginType.CONSUME_RANGE
    margin.save()
    assert generator.get_default_margin_rate(rate=margin.rate) is None


@pytest.mark.django_db
def test_get_default_margin_rate_consume_range_no_annual_consumption(
    saving_study, margin
):
    saving_study.annual_consumption = None
    generator = SuggestedRatesGenerator(saving_study)
    margin.type = MarginType.CONSUME_RANGE
    margin.min_consumption = Decimal(1)
    margin.save()
    assert generator.get_default_margin_rate(rate=margin.rate) == margin


@pytest.mark.django_db
def test_get_default_margin_rate_consume_range(saving_study, margin):
    saving_study.annual_consumption = Decimal(100)
    generator = SuggestedRatesGenerator(saving_study)
    margin.type = MarginType.CONSUME_RANGE
    margin.min_consumption = Decimal(10)
    margin.max_consumption = Decimal(1000)
    margin.save()
    assert generator.get_default_margin_rate(rate=margin.rate) == margin


@pytest.mark.django_db
def test_get_default_margin_rate_consume_range_multiple_margins(
    saving_study, rate, margin
):
    Margin.objects.create(
        rate=rate,
        type=MarginType.CONSUME_RANGE,
        min_consumption=Decimal(10),
        max_consumption=Decimal(1000),
    )
    saving_study.annual_consumption = Decimal(100)
    generator = SuggestedRatesGenerator(saving_study)
    margin.type = MarginType.CONSUME_RANGE
    margin.min_consumption = Decimal(10)
    margin.max_consumption = Decimal(1000)
    margin.save()
    assert generator.get_default_margin_rate(rate=margin.rate) is None


@pytest.mark.django_db
def test_get_margin_with_min_consumption_is_none(saving_study, rate):
    Margin.objects.create(
        rate=rate,
        type=MarginType.CONSUME_RANGE,
        min_consumption=None,
        max_consumption=None,
    )
    generator = SuggestedRatesGenerator(saving_study)
    qs = Margin.objects.all()
    assert generator.get_margin_with_min_consumption(qs) is None


@pytest.mark.django_db
def test_get_margin_with_min_consumption_is_not_none(saving_study, rate):
    margin_minor = Margin.objects.create(
        rate=rate,
        type=MarginType.CONSUME_RANGE,
        min_consumption=Decimal(1),
        max_consumption=None,
    )
    generator = SuggestedRatesGenerator(saving_study)
    qs = Margin.objects.all()
    assert generator.get_margin_with_min_consumption(qs) == margin_minor


@pytest.mark.django_db
def test_get_margin_with_min_consumption(saving_study, rate):
    margin_minor = Margin.objects.create(
        rate=rate,
        type=MarginType.CONSUME_RANGE,
        min_consumption=Decimal(1),
        max_consumption=None,
    )
    Margin.objects.create(
        rate=rate,
        type=MarginType.CONSUME_RANGE,
        min_consumption=Decimal(10),
        max_consumption=None,
    )
    generator = SuggestedRatesGenerator(saving_study)
    qs = Margin.objects.all()
    assert generator.get_margin_with_min_consumption(qs) == margin_minor


@pytest.mark.django_db
def test_generate_suggested_rates_no_rates(saving_study):
    generator = SuggestedRatesGenerator(saving_study)
    qs = Rate.objects.none()
    assert generator.generate_suggested_rates(qs).count() == 0


@pytest.mark.django_db
def test_generate_suggested_rates(saving_study, rate):
    generator = SuggestedRatesGenerator(saving_study)
    qs = Rate.objects.all()
    assert generator.generate_suggested_rates(qs).count() == 1


@pytest.mark.django_db
def test_compute_current_cost(saving_study):
    saving_study.energy_type = EnergyTypes.ELECTRICITY
    generator = SuggestedRatesGenerator(saving_study)
    assert generator.compute_current_cost() == Money(
        0, currency=settings.DEFAULT_CURRENCY
    )
