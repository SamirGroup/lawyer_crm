from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from invoice.models import Invoice
from contact.models import Request


def demo_pay(request, invoice_id, method):
    """
    Simulates a Payme/Click payment page for demo/testing.
    GET  → show confirmation page
    POST → mark invoice paid and redirect to cabinet
    """
    inv = get_object_or_404(Invoice, pk=invoice_id)

    if request.method == 'POST':
        if not inv.paid:
            inv.paid = True
            inv.paid_date = timezone.now()
            inv.paid_amount = inv.ten_percent_amount
            inv.payment_method = method
            inv.save()
            inv.request.status = Request.STATUS_PAID
            inv.request.save(update_fields=['status'])
        return redirect(f'/cabinet/{inv.request_id}/')

    return render(request, 'payment/demo_pay.html', {
        'inv': inv,
        'method': method,
        'method_label': 'Payme' if method == 'payme' else 'Click',
    })
