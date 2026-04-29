from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from django.conf import settings
from contact.models import Request
from .models import Invoice


@csrf_exempt
@require_http_methods(["POST"])
def create_invoice(request_http, pk):
    """Admin creates invoice for a request."""
    from django.contrib.auth.decorators import login_required
    if not request_http.user.is_authenticated or not request_http.user.is_admin():
        return JsonResponse({'error': 'Forbidden'}, status=403)

    req = get_object_or_404(Request, pk=pk)
    if not req.total_amount:
        return JsonResponse({'error': 'Set total_amount first'}, status=400)

    if hasattr(req, 'invoice'):
        inv = req.invoice
    else:
        inv = Invoice.objects.create(
            request=req,
            invoice_number=Invoice.generate_number(),
            ten_percent_amount=req.minimum_payment(),
        )
        req.status = Request.STATUS_OFFERED
        req.save(update_fields=['status'])

    return JsonResponse({
        'invoice_number': inv.invoice_number,
        'amount': str(inv.ten_percent_amount),
        'paid': inv.paid,
    })


@require_http_methods(["GET"])
def get_invoice(request_http, pk):
    inv = get_object_or_404(Invoice, pk=pk)
    payme_url = _payme_url(inv)
    click_url = _click_url(inv)
    return JsonResponse({
        'invoice_number': inv.invoice_number,
        'amount': str(inv.ten_percent_amount),
        'paid': inv.paid,
        'paid_date': inv.paid_date.isoformat() if inv.paid_date else None,
        'payme_url': payme_url,
        'click_url': click_url,
    })


def _payme_url(inv):
    import base64
    merchant_id = settings.PAYME_MERCHANT_ID
    amount_tiyin = int(inv.ten_percent_amount * 100)
    host = 'checkout.test.paycom.uz' if settings.PAYME_TEST_MODE else 'checkout.paycom.uz'
    params = f"m={merchant_id};ac.invoice_id={inv.pk};a={amount_tiyin};l=ru"
    encoded = base64.b64encode(params.encode()).decode()
    return f"https://{host}/{encoded}"


def _click_url(inv):
    service_id = settings.CLICK_SERVICE_ID
    merchant_id = settings.CLICK_MERCHANT_ID
    amount = int(inv.ten_percent_amount)
    return (
        f"https://my.click.uz/services/pay?service_id={service_id}"
        f"&merchant_id={merchant_id}&amount={amount}"
        f"&transaction_param={inv.pk}&return_url=http://localhost:8000/cabinet/{inv.request_id}/"
    )
