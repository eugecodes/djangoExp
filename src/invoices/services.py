from auditlog.context import set_actor
from django.contrib.auth import get_user_model
from djmoney.money import Money
from guardian.shortcuts import get_objects_for_user
from ninja import FilterSchema
from ninja.errors import AuthenticationError

from common.api.requests import DeleteRequest
from common.services import model_update, delete_models, detail_model
from invoices.api.schemas.requests import InvoiceRequest, InvoiceUpdateRequest
from invoices.models import Invoice
from invoices.permissions import InvoicePermissions

User = get_user_model()


def invoice_list(filters: FilterSchema, actor: User):
    if actor.is_superuser:
        invoices = Invoice.objects.all()
    else:
        invoices = get_objects_for_user(actor, InvoicePermissions.READ)
    invoices = filters.filter(invoices)
    return invoices


def invoice_create(data: InvoiceRequest, actor: User):
    if not actor.has_perm(InvoicePermissions.CREATE) and not actor.is_superuser:
        raise AuthenticationError
    with set_actor(actor):
        data.base_price = Money(
            data.base_price_amount,
            currency=data.base_price_currency,
        )
        del (data.base_price_amount, data.base_price_currency)
        data.vat = Money(
            data.vat_amount,
            currency=data.vat_currency,
        )
        del (data.vat_amount, data.vat_currency)
        data.total = Money(
            data.base_price.amount + data.vat.amount, data.base_price.currency
        )
        invoice = Invoice.objects.create(**data.dict())
    return invoice


def invoice_update(
    invoice: Invoice, data: InvoiceUpdateRequest, actor: User
) -> Invoice:
    if not actor.has_perm(InvoicePermissions.EDIT, invoice) and not actor.is_superuser:
        raise AuthenticationError
    data.base_price = Money(
        data.base_price_amount,
        currency=data.base_price_currency,
    )
    del (data.base_price_amount, data.base_price_currency)
    data.vat = Money(
        data.vat_amount,
        currency=data.vat_currency,
    )
    del (data.vat_amount, data.vat_currency)
    data.total = Money(
        data.base_price.amount + data.vat.amount, data.base_price.currency
    )
    return model_update(invoice, data, actor)


def invoice_detail(invoice: Invoice, actor: User) -> Invoice:
    return detail_model(actor, InvoicePermissions.READ, invoice)


def delete_invoices(data: DeleteRequest, actor: User):
    delete_models(actor, InvoicePermissions.DELETE, data)
