import json
import hashlib
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.utils import timezone
from invoice.models import Invoice
from contact.models import Request


def _mark_paid(inv, method, amount):
    if not inv.paid:
        inv.paid = True
        inv.paid_date = timezone.now()
        inv.paid_amount = amount
        inv.payment_method = method
        inv.save()
        inv.request.status = Request.STATUS_PAID
        inv.request.save(update_fields=['status'])


# ── Payme ──────────────────────────────────────────────────────────────────────

PAYME_METHODS = {
    'CheckPerformTransaction', 'CreateTransaction',
    'PerformTransaction', 'CancelTransaction', 'CheckTransaction',
}


@csrf_exempt
@require_http_methods(["POST"])
def payme_webhook(request):
    auth = request.headers.get('Authorization', '')
    expected = f"Basic {_payme_auth_token()}"
    if auth != expected:
        return JsonResponse({'error': {'code': -32504, 'message': 'Forbidden'}}, status=403)

    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': {'code': -32700, 'message': 'Parse error'}}, status=400)

    method = body.get('method')
    params = body.get('params', {})
    req_id = body.get('id', 1)

    if method not in PAYME_METHODS:
        return JsonResponse({'error': {'code': -32601, 'message': 'Method not found'}})

    invoice_id = params.get('account', {}).get('invoice_id')
    try:
        inv = Invoice.objects.get(pk=invoice_id)
    except Invoice.DoesNotExist:
        return JsonResponse({'id': req_id, 'error': {'code': -31050, 'message': 'Invoice not found'}})

    amount_tiyin = params.get('amount', 0)
    amount = amount_tiyin / 100

    if method == 'CheckPerformTransaction':
        if amount < float(inv.ten_percent_amount):
            return JsonResponse({'id': req_id, 'error': {'code': -31001, 'message': 'Insufficient amount'}})
        return JsonResponse({'id': req_id, 'result': {'allow': True}})

    if method in ('CreateTransaction', 'PerformTransaction'):
        _mark_paid(inv, 'payme', amount)
        return JsonResponse({'id': req_id, 'result': {'transaction': str(inv.pk), 'perform_time': int(timezone.now().timestamp() * 1000), 'state': 2}})

    if method == 'CheckTransaction':
        return JsonResponse({'id': req_id, 'result': {'state': 2 if inv.paid else 1}})

    return JsonResponse({'id': req_id, 'result': {}})


def _payme_auth_token():
    import base64
    creds = f"{settings.PAYME_MERCHANT_ID}:{settings.PAYME_SECRET_KEY}"
    return base64.b64encode(creds.encode()).decode()


# ── Click ──────────────────────────────────────────────────────────────────────

@csrf_exempt
@require_http_methods(["POST"])
def click_webhook(request):
    """Click PREPARE and COMPLETE handlers."""
    service_id = request.POST.get('service_id')
    click_trans_id = request.POST.get('click_trans_id')
    merchant_trans_id = request.POST.get('merchant_trans_id')  # invoice pk
    amount = request.POST.get('amount')
    action = request.POST.get('action')  # 0=prepare, 1=complete
    sign_time = request.POST.get('sign_time', '')
    sign_string = request.POST.get('sign_string', '')

    expected_sign = hashlib.md5(
        f"{click_trans_id}{service_id}{settings.CLICK_SECRET_KEY}{merchant_trans_id}{amount}{action}{sign_time}".encode()
    ).hexdigest()

    if sign_string != expected_sign:
        return JsonResponse({'error': -1, 'error_note': 'Invalid sign'})

    try:
        inv = Invoice.objects.get(pk=merchant_trans_id)
    except Invoice.DoesNotExist:
        return JsonResponse({'error': -5, 'error_note': 'Invoice not found'})

    if action == '1':
        _mark_paid(inv, 'click', float(amount))

    return JsonResponse({
        'click_trans_id': click_trans_id,
        'merchant_trans_id': merchant_trans_id,
        'merchant_confirm_id': inv.pk,
        'error': 0,
        'error_note': 'Success',
    })
