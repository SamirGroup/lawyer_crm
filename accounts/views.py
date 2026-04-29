from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from chat.models import Case


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if user.is_admin():
                return redirect('/admin-panel/')
            return redirect('/lawyer/')
        return render(request, 'accounts/login.html', {'error': 'Invalid credentials'})
    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('/accounts/login/')


@login_required
def lawyer_office(request):
    if not request.user.is_lawyer():
        return redirect('/admin-panel/')
    lawyer = request.user.lawyer_profile
    cases = Case.objects.filter(lawyer=lawyer).select_related('request')
    status_filter = request.GET.get('status')
    if status_filter:
        cases = cases.filter(status=status_filter)
    return render(request, 'lawyer/office.html', {
        'cases': cases,
        'lawyer': lawyer,
        'statuses': Case.STATUSES,
        'current_status': status_filter,
    })


@login_required
def lawyer_case(request, case_id):
    if not request.user.is_lawyer():
        return redirect('/admin-panel/')
    case = get_object_or_404(Case, pk=case_id, lawyer__user=request.user)
    return render(request, 'lawyer/case.html', {'case': case, 'statuses': Case.STATUSES})
