import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from .models import Request


def _allowed_file(name):
    ext = name.rsplit('.', 1)[-1].lower() if '.' in name else ''
    return ext in settings.ALLOWED_FILE_EXTENSIONS


@csrf_exempt
@require_http_methods(["POST"])
def create_request(request):
    name = request.POST.get('customer_name', '').strip()
    phone = request.POST.get('phone', '').strip()
    text = request.POST.get('text', '').strip()
    if not all([name, phone, text]):
        return JsonResponse({'error': 'name, phone and text are required'}, status=400)
    file = request.FILES.get('file')
    if file and not _allowed_file(file.name):
        return JsonResponse({'error': 'File type not allowed'}, status=400)
    if file and file.size > settings.MAX_UPLOAD_SIZE:
        return JsonResponse({'error': 'File too large'}, status=400)
    req = Request.objects.create(
        customer_name=name, phone=phone, text=text,
        file=file, source=Request.SOURCE_SITE,
    )
    return JsonResponse({
        'id': req.pk,
        'token': str(req.access_token),
        'cabinet_url': f'/cabinet/{req.access_token}/',
        'message': 'Request submitted successfully',
    }, status=201)


@require_http_methods(["GET"])
def get_request(request, pk):
    req = get_object_or_404(Request, pk=pk)
    inv = getattr(req, 'invoice', None)
    return JsonResponse({
        'id': req.pk,
        'status': req.status,
        'direction': req.direction,
        'total_amount': str(req.total_amount) if req.total_amount else None,
        'minimum_payment': str(req.minimum_payment()) if req.minimum_payment() else None,
        'has_invoice': inv is not None,
        'paid': inv.paid if inv else False,
        'invoice_number': inv.invoice_number if inv else None,
        'cabinet_url': f'/cabinet/{req.access_token}/',
    })


def home(request):
    return render(request, 'client/home.html')


def status_page(request):
    return render(request, 'client/status.html')


def payment_bare(request):
    return redirect('/status/')


def cabinet_bare(request):
    return redirect('/status/')


def payment_page(request, pk):
    req = get_object_or_404(Request, pk=pk)
    invoice = getattr(req, 'invoice', None)
    return render(request, 'client/payment.html', {
        'req': req, 'invoice': invoice,
        'demo_mode': getattr(settings, 'DEMO_MODE', False),
    })


def cabinet(request, token):
    req = get_object_or_404(Request, access_token=token)
    case = getattr(req, 'case', None)
    invoice = getattr(req, 'invoice', None)
    return render(request, 'client/cabinet.html', {
        'req': req, 'case': case, 'invoice': invoice,
        'token': str(token),
        'demo_mode': getattr(settings, 'DEMO_MODE', False),
    })
