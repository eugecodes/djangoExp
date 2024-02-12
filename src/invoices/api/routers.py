from typing import List

from django.http import FileResponse
from django.shortcuts import get_object_or_404
from ninja import Router, Query
from ninja.pagination import paginate

from common.api.requests import DeleteRequest
from common.export import generate_csv_file
from common.pagination import CustomPagination
from invoices.api.schemas.exports import invoice_export_headers
from invoices.api.schemas.requests import InvoiceRequest, InvoiceUpdateRequest
from invoices.api.schemas.filters import InvoiceFilterSchema
from invoices.api.schemas.responses import (
    InvoiceListResponse,
    BasicInvoiceResponse,
)
from invoices.services import (
    invoice_create,
    invoice_update,
    delete_invoices,
    invoice_list,
    invoice_detail,
)
from invoices.models import Invoice

router = Router()


@router.get("", response=List[InvoiceListResponse])
@paginate(CustomPagination)
def invoice_list_endpoint(request, filters: InvoiceFilterSchema = Query(...)):
    return invoice_list(filters, request.user)


@router.post("", response={201: BasicInvoiceResponse})
def invoice_create_endpoint(request, payload: InvoiceRequest):
    return invoice_create(payload, request.user)


@router.put("/{invoice_id}", response=BasicInvoiceResponse)
def invoice_update_endpoint(request, invoice_id: int, payload: InvoiceUpdateRequest):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    return invoice_update(invoice, payload, request.user)


@router.patch("/{invoice_id}", response=BasicInvoiceResponse)
def invoice_update_partial_endpoint(request, invoice_id: int, payload: InvoiceUpdateRequest):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    return invoice_update(invoice, payload, request.user)


@router.get("/{invoice_id}", response=BasicInvoiceResponse)
def invoice_detail_endpoint(request, invoice_id: int):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    return invoice_detail(invoice, request.user)


@router.post("/delete/")
def delete_invoice_endpoint(request, payload: DeleteRequest):
    delete_invoices(payload, request.user)


@router.post("/export/csv/")
def invoice_export_endpoint(request):
    return FileResponse(
        generate_csv_file("invoice", invoice_export_headers, Invoice.objects.all())
    )
