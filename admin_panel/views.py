import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db.models import Count, Q
from contact.models import Request
from invoice.models import Invoice
from accounts.models import User, Lawyer
from chat.models import Case


def admin_required(view_func):
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.is_admin():
            return redirect('/accounts/login/')
        return view_func(request, *args, **kwargs)
    return wrapper


@admin_required
def dashboard(request):
    stats = {
        'total': Request.objects.count(),
        'new': Request.objects.filter(status='new').count(),
        'paid': Request.objects.filter(status='paid').count(),
        'assigned': Request.objects.filter(status='assigned').count(),
        'closed': Request.objects.filter(status='closed').count(),
        'lawyers': Lawyer.objects.count(),
    }
    recent = Request.objects.all()[:10]
    return render(request, 'admin_panel/dashboard.html', {'stats': stats, 'recent': recent})


@admin_required
def requests_list(request):
    qs = Request.objects.all()
    status = request.GET.get('status')
    source = request.GET.get('source')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    search = request.GET.get('search', '')

    if status:
        qs = qs.filter(status=status)
    if source:
        qs = qs.filter(source=source)
    if date_from:
        qs = qs.filter(date__date__gte=date_from)
    if date_to:
        qs = qs.filter(date__date__lte=date_to)
    if search:
        qs = qs.filter(Q(customer_name__icontains=search) | Q(phone__icontains=search))

    return render(request, 'admin_panel/requests.html', {
        'requests': qs,
        'statuses': Request.STATUSES,
        'sources': Request.SOURCES,
    })


@admin_required
def request_detail(request, pk):
    req = get_object_or_404(Request, pk=pk)
    lawyers = Lawyer.objects.select_related('user').all()
    case = getattr(req, 'case', None)
    invoice = getattr(req, 'invoice', None)
    return render(request, 'admin_panel/request_detail.html', {
        'req': req,
        'lawyers': lawyers,
        'case': case,
        'invoice': invoice,
        'directions': Request.DIRECTIONS,
        'statuses': Request.STATUSES,
    })


@csrf_exempt
@admin_required
@require_http_methods(["POST"])
def update_request(request, pk):
    req = get_object_or_404(Request, pk=pk)
    data = json.loads(request.body)

    if 'direction' in data:
        req.direction = data['direction']
    if 'total_amount' in data:
        val = data['total_amount']
        req.total_amount = val if val not in (None, '', 'null') else None
    if 'admin_comment' in data:
        req.admin_comment = data['admin_comment']
    if 'status' in data:
        req.status = data['status']
    req.save()
    return JsonResponse({'ok': True})


@csrf_exempt
@admin_required
@require_http_methods(["POST"])
def create_invoice_admin(request, pk):
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
    return JsonResponse({'invoice_number': inv.invoice_number, 'amount': str(inv.ten_percent_amount)})


@csrf_exempt
@admin_required
@require_http_methods(["POST"])
def assign_lawyer(request, pk):
    req = get_object_or_404(Request, pk=pk)
    data = json.loads(request.body)
    lawyer_id = data.get('lawyer_id')
    lawyer = get_object_or_404(Lawyer, pk=lawyer_id)

    case, created = Case.objects.get_or_create(request=req, defaults={'lawyer': lawyer})
    if not created:
        case.lawyer = lawyer
        case.save(update_fields=['lawyer'])

    req.status = Request.STATUS_ASSIGNED
    req.save(update_fields=['status'])
    return JsonResponse({'ok': True, 'case_id': case.pk})


@admin_required
def lawyers_list(request):
    lawyers = Lawyer.objects.select_related('user').all()
    return render(request, 'admin_panel/lawyers.html', {'lawyers': lawyers})


@csrf_exempt
@admin_required
@require_http_methods(["POST"])
def add_lawyer(request):
    data = json.loads(request.body)
    user = User.objects.create_user(
        username=data['username'],
        password=data['password'],
        first_name=data.get('first_name', ''),
        last_name=data.get('last_name', ''),
        role=User.ROLE_LAWYER,
    )
    Lawyer.objects.create(
        user=user,
        direction=data.get('direction', 'other'),
        phone=data.get('phone', ''),
        telegram_id=data.get('telegram_id', ''),
    )
    return JsonResponse({'ok': True, 'id': user.pk})


@csrf_exempt
@admin_required
@require_http_methods(["POST"])
def delete_lawyer(request, pk):
    lawyer = get_object_or_404(Lawyer, pk=pk)
    lawyer.user.delete()
    return JsonResponse({'ok': True})
