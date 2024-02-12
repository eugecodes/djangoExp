from decimal import Decimal
from uuid import uuid4

import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from djmoney.money import Money
from guardian.shortcuts import assign_perm
from ninja.testing import TestClient

from addresses.models import Address
from addresses.permissions import AddressPermissions
from channels.models import Channel
from clients.choices import ClientTypes
from clients.models import Client
from clients.permissions import ClientPermissions
from commissions.models import Commission
from common.choices import EnergyTypes
from config.api import api
from contacts.models import Contact
from contacts.permissions import ContactPermissions
from contracts.models import Contract
from contracts.permissions import ContractPermissions
from costs.models import OtherCost
from energy_costs.constants import VAT, VAT_REDUCED, ELECTRICITY_TAX, OIL_TAX
from energy_costs.models import EnergyCost
from invoices.models import Invoice
from invoices.permissions import InvoicePermissions
from margins.models import Margin
from marketers.models import Marketer
from rate_types.models import RateType
from rates.choices import PriceTypes
from rates.models import Rate
from roles.models import Role
from roles.permissions import RolePermissions
from saving_studies.models import SavingStudy
from saving_studies.permissions import SavingStudyPermissions
from suggested_rates.models import SuggestedRate
from suggested_rates.permissions import SuggestedRatePermissions
from supply_points.models import SupplyPoint
from supply_points.permissions import SupplyPointPermissions

User = get_user_model()

PASSWORD = "Contraseña1"


def group_creation():
    channel_support_group, created = Group.objects.get_or_create(
        name=settings.DEFAULT_CHANNEL_SUPPORT,
    )
    Role.objects.get_or_create(
        name=settings.DEFAULT_CHANNEL_SUPPORT, group=channel_support_group
    )
    backoffice_group, created = Group.objects.get_or_create(
        name=settings.DEFAULT_BACKOFFICE,
    )
    Role.objects.get_or_create(name=settings.DEFAULT_BACKOFFICE, group=backoffice_group)


def tax_creation():
    EnergyCost.objects.get_or_create(
        concept="IVA (%)",
        amount=21,
        code=VAT,
    )
    EnergyCost.objects.get_or_create(
        concept="IVA Reducido (%)",
        amount=5,
        code=VAT_REDUCED,
    )
    EnergyCost.objects.get_or_create(
        concept="Impuestos de hidrocarburos (€/kWh)",
        amount=0.00234,
        code=OIL_TAX,
    )
    EnergyCost.objects.get_or_create(
        concept="Impuestos eléctricos (%)",
        amount=5.1127,
        code=ELECTRICITY_TAX,
    )


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        group_creation()
        tax_creation()


@pytest.fixture
def client():
    client = TestClient(api)
    yield client


@pytest.fixture
@pytest.mark.django_db
def admin_user():
    user = User.objects.create(
        email=f"testuser-{uuid4()}@test.es",
        is_superuser=True,
        channel=None,
    )
    yield user


@pytest.fixture
@pytest.mark.django_db
def channel():
    channel = Channel.objects.create(
        name=f"channel", social_name="social_name", cif="12345678Z"
    )
    yield channel


@pytest.fixture
@pytest.mark.django_db
def channel_admin(channel, admin_channel_role):
    role, group = admin_channel_role
    user = User.objects.create(
        email=f"testuser-{uuid4()}@test.es",
        channel=channel,
        is_superuser=False,
        is_staff=False,
    )
    user.groups.add(group)

    assign_perm(ClientPermissions.CREATE, group)

    yield user


@pytest.fixture
@pytest.mark.django_db
def channel_user(channel, user_channel_role):
    user = User.objects.create(
        email=f"testuser-{uuid4()}@test.es",
        channel=channel,
        is_superuser=False,
        is_staff=False,
    )
    user.groups.add(user_channel_role[1])

    yield user


@pytest.fixture
@pytest.mark.django_db
def role():
    group = Group.objects.create(
        name=f"role_name",
    )
    role = Role.objects.create(name="role_name", group=group)
    yield role


@pytest.fixture
@pytest.mark.django_db
def admin_channel_role(channel):
    group = Group.objects.create(
        name=f"{channel.name} - admin",
    )
    role = Role.objects.create(
        name=f"{channel.name} - admin", group=group, channel=channel, admin_role=True
    )
    assign_perm(RolePermissions.READ, group, role)
    assign_perm(RolePermissions.EDIT, group, role)
    assign_perm(RolePermissions.DELETE, group, role)
    assign_perm(RolePermissions.CREATE, group)
    assign_perm(SavingStudyPermissions.CREATE, group)
    assign_perm(ContractPermissions.CREATE, group)
    assign_perm(AddressPermissions.CREATE, group)
    assign_perm(SupplyPointPermissions.CREATE, group)
    assign_perm(ContactPermissions.CREATE, group)
    assign_perm(InvoicePermissions.CREATE, group)
    yield role, group


@pytest.fixture
@pytest.mark.django_db
def user_channel_role(channel):
    group = Group.objects.create(
        name=f"{channel.name} - user",
    )
    role = Role.objects.create(
        name=f"{channel.name} - user", group=group, channel=channel, admin_role=False
    )
    assign_perm(RolePermissions.READ, group, role)
    yield role, group


@pytest.fixture
@pytest.mark.django_db
def channel_client(channel, admin_channel_role):
    client = Client.objects.create(alias=f"{channel.name} - client", channel=channel)
    role, group = admin_channel_role
    assign_perm(ClientPermissions.READ, group, client)
    assign_perm(ClientPermissions.EDIT, group, client)
    assign_perm(ClientPermissions.DELETE, group, client)
    yield client


@pytest.fixture
@pytest.mark.django_db
def marketer(address):
    marketer = Marketer.objects.create(name="Marketer", address=address)
    yield marketer


@pytest.fixture
@pytest.mark.django_db
def rate_type():
    rate_type = RateType.objects.create(
        name="Rate Type",
        max_power=10,
        min_power=10,
        energy_type=EnergyTypes.ELECTRICITY,
    )
    yield rate_type


@pytest.fixture
@pytest.mark.django_db
def rate(marketer, rate_type):
    rate = Rate.objects.create(
        name="Rate",
        permanency=True,
        length=12,
        marketer=marketer,
        rate_type=rate_type,
        price_type=PriceTypes.BASE,
        client_types=[ClientTypes.COMPANY],
    )
    yield rate


@pytest.fixture
@pytest.mark.django_db
def margin(marketer, rate):
    margin = Margin.objects.create(rate=rate)
    yield margin


@pytest.fixture
@pytest.mark.django_db
def commission(rate_type):
    commission = Commission.objects.create(name="Test", rate_type=rate_type)
    yield commission


@pytest.fixture
@pytest.mark.django_db
def saving_study(admin_channel_role, channel):
    saving_study = SavingStudy.objects.create(
        channel=channel,
        power_1=Decimal(0),
        power_2=Decimal(0),
        power_3=Decimal(0),
        power_4=Decimal(0),
        power_5=Decimal(0),
        power_6=Decimal(0),
        consumption_p1=Decimal(0),
        consumption_p2=Decimal(0),
        consumption_p3=Decimal(0),
        consumption_p4=Decimal(0),
        consumption_p5=Decimal(0),
        consumption_p6=Decimal(0),
    )
    role, group = admin_channel_role
    assign_perm(SavingStudyPermissions.READ, group, saving_study)
    assign_perm(SavingStudyPermissions.EDIT, group, saving_study)
    assign_perm(SavingStudyPermissions.DELETE, group, saving_study)
    yield saving_study


@pytest.fixture
@pytest.mark.django_db
def contract(admin_channel_role, channel, channel_client, rate, supply_point):
    contract = Contract.objects.create(
        channel=channel, client=channel_client, rate=rate, supply_point=supply_point
    )
    role, group = admin_channel_role
    assign_perm(ContractPermissions.READ, group, contract)
    assign_perm(ContractPermissions.EDIT, group, contract)
    assign_perm(ContractPermissions.DELETE, group, contract)
    yield contract


@pytest.fixture
@pytest.mark.django_db
def address(admin_channel_role, channel):
    address = Address.objects.create(channel=channel)
    role, group = admin_channel_role
    assign_perm(AddressPermissions.READ, group, address)
    assign_perm(AddressPermissions.EDIT, group, address)
    assign_perm(AddressPermissions.DELETE, group, address)
    yield address


@pytest.fixture
@pytest.mark.django_db
def supply_point(admin_channel_role, channel, channel_client, address):
    supply_point = SupplyPoint.objects.create(
        channel=channel, client=channel_client, address=address, counter_price=0
    )
    role, group = admin_channel_role
    assign_perm(SupplyPointPermissions.READ, group, supply_point)
    assign_perm(SupplyPointPermissions.EDIT, group, supply_point)
    assign_perm(SupplyPointPermissions.DELETE, group, supply_point)
    yield supply_point


@pytest.fixture
@pytest.mark.django_db
def contact(admin_channel_role, channel_client):
    contact = Contact.objects.create(client=channel_client)
    role, group = admin_channel_role
    assign_perm(ContactPermissions.READ, group, contact)
    assign_perm(ContactPermissions.EDIT, group, contact)
    assign_perm(ContactPermissions.DELETE, group, contact)
    yield contact


@pytest.fixture
@pytest.mark.django_db
def cost():
    cost = OtherCost.objects.create(
        name="test", mandatory=True, client_types=[ClientTypes.COMPANY], quantity=1
    )
    yield cost


@pytest.fixture
@pytest.mark.django_db
def energy_cost():
    energy_cost = EnergyCost.objects.create(concept="test", amount=10, code="test")
    yield energy_cost


@pytest.fixture
@pytest.mark.django_db
def invoice(admin_channel_role, channel):
    invoice = Invoice.objects.create(
        channel=channel,
        invoice_date="2024-12-12",
        base_price=Money(1, currency=settings.DEFAULT_CURRENCY),
        vat=Money(1, currency=settings.DEFAULT_CURRENCY),
        total=Money(1, currency=settings.DEFAULT_CURRENCY),
    )
    role, group = admin_channel_role
    assign_perm(InvoicePermissions.READ, group, invoice)
    assign_perm(InvoicePermissions.EDIT, group, invoice)
    assign_perm(InvoicePermissions.DELETE, group, invoice)
    yield invoice


@pytest.fixture
@pytest.mark.django_db
def suggested_rate(admin_channel_role, channel, saving_study):
    suggested_rate = SuggestedRate.objects.create(
        channel=channel,
        saving_study=saving_study,
        has_contractual_commitment=True,
        duration=1,
        is_full_renewable=True,
        has_net_metering=True,
        net_metering_value=Money(1, currency=settings.DEFAULT_CURRENCY),
        min_profit_margin=Money(1, currency=settings.DEFAULT_CURRENCY),
        max_profit_margin=Money(1, currency=settings.DEFAULT_CURRENCY),
        applied_profit_margin=Money(1, currency=settings.DEFAULT_CURRENCY),
    )
    role, group = admin_channel_role
    assign_perm(SuggestedRatePermissions.READ, group, suggested_rate)
    assign_perm(SuggestedRatePermissions.EDIT, group, suggested_rate)
    assign_perm(SuggestedRatePermissions.DELETE, group, suggested_rate)
    yield suggested_rate
