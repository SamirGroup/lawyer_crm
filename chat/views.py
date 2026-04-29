import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from django.conf import settings
from .models import Case, Message, Meeting, PreCaseMessage


def _msg_dict(m, is_pre=False):
    return {
        'id': m.pk,
        'sender': 'client' if is_pre else m.sender,
        'sender_name': m.request.customer_name if is_pre else m.sender_name,
        'text': m.text,
        'file': m.file.url if m.file else None,
        'timestamp': m.timestamp.isoformat(),
        'is_pre': is_pre,
    }


def _get_request_by_token(token):
    from contact.models import Request
    return Request.objects.filter(access_token=token).first()


@csrf_exempt
@require_http_methods(["POST"])
def send_message(request):
    sender = request.POST.get('sender', '').strip()
    text = request.POST.get('text', '').strip()
    file = request.FILES.get('file')

    if file:
        ext = file.name.rsplit('.', 1)[-1].lower() if '.' in file.name else ''
        if ext not in settings.ALLOWED_FILE_EXTENSIONS:
            return JsonResponse({'error': 'File type not allowed'}, status=400)

    if not text and not file:
        return JsonResponse({'error': 'Message or file required'}, status=400)

    if sender == 'client':
        token = request.POST.get('token', '')
        req = _get_request_by_token(token)
        if not req:
            return JsonResponse({'error': 'Invalid token'}, status=403)
        if hasattr(req, 'case'):
            msg = Message.objects.create(
                case=req.case, sender='client',
                sender_name=req.customer_name, text=text, file=file
            )
            return JsonResponse(_msg_dict(msg), status=201)
        else:
            pre = PreCaseMessage.objects.create(request=req, text=text, file=file)
            return JsonResponse(_msg_dict(pre, is_pre=True), status=201)

    elif sender in ('lawyer', 'admin'):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Login required'}, status=403)
        case = get_object_or_404(Case, pk=request.POST.get('case_id', ''))
        sender_name = request.user.get_full_name() or request.user.username
        msg = Message.objects.create(
            case=case, sender=sender, sender_name=sender_name, text=text, file=file
        )
        return JsonResponse(_msg_dict(msg), status=201)

    return JsonResponse({'error': 'Invalid sender'}, status=400)


@require_http_methods(["GET"])
def get_messages(request, case_id):
    if request.user.is_authenticated:
        case = get_object_or_404(Case, pk=case_id)
        req = case.request
    else:
        token = request.GET.get('token', '')
        req = _get_request_by_token(token)
        if not req or not hasattr(req, 'case') or req.case.pk != int(case_id):
            return JsonResponse({'error': 'Forbidden'}, status=403)
        case = req.case

    since = request.GET.get('since')
    pre_msgs = [_msg_dict(m, is_pre=True) for m in req.pre_messages.all()]
    case_qs = case.messages.all()
    if since:
        case_qs = case_qs.filter(pk__gt=int(since))
    case_msgs = [_msg_dict(m) for m in case_qs]
    all_msgs = sorted(pre_msgs + case_msgs, key=lambda x: x['timestamp'])
    return JsonResponse({'messages': all_msgs})


@require_http_methods(["GET"])
def get_pre_messages(request):
    token = request.GET.get('token', '')
    req = _get_request_by_token(token)
    if not req:
        return JsonResponse({'error': 'Invalid token'}, status=403)
    since = request.GET.get('since')
    qs = req.pre_messages.all()
    if since:
        qs = qs.filter(pk__gt=int(since))
    return JsonResponse({'messages': [_msg_dict(m, is_pre=True) for m in qs]})


@require_http_methods(["GET"])
def admin_monitor_chat(request, case_id):
    if not request.user.is_authenticated or not request.user.is_admin():
        return JsonResponse({'error': 'Forbidden'}, status=403)
    case = get_object_or_404(Case, pk=case_id)
    req = case.request
    since = request.GET.get('since')
    pre_msgs = [_msg_dict(m, is_pre=True) for m in req.pre_messages.all()]
    case_qs = case.messages.all()
    if since:
        case_qs = case_qs.filter(pk__gt=int(since))
    all_msgs = sorted(pre_msgs + [_msg_dict(m) for m in case_qs], key=lambda x: x['timestamp'])
    return JsonResponse({'messages': all_msgs})


@csrf_exempt
@require_http_methods(["POST"])
def update_case_status(request, case_id):
    if not request.user.is_authenticated or not request.user.is_lawyer():
        return JsonResponse({'error': 'Forbidden'}, status=403)
    case = get_object_or_404(Case, pk=case_id, lawyer__user=request.user)
    data = json.loads(request.body)
    status = data.get('status')
    if status not in dict(Case.STATUSES):
        return JsonResponse({'error': 'Invalid status'}, status=400)
    case.status = status
    if 'notes' in data:
        case.notes = data['notes']
    case.save()
    return JsonResponse({'status': case.status})


@require_http_methods(["GET"])
def get_meetings(request, case_id):
    if not request.user.is_authenticated:
        token = request.GET.get('token', '')
        req = _get_request_by_token(token)
        if not req or not hasattr(req, 'case') or req.case.pk != int(case_id):
            return JsonResponse({'error': 'Forbidden'}, status=403)
        case = req.case
    else:
        case = get_object_or_404(Case, pk=case_id)
    return JsonResponse({'meetings': [
        {'id': m.pk, 'title': m.title, 'meeting_type': m.meeting_type,
         'scheduled_at': m.scheduled_at.isoformat(), 'duration_minutes': m.duration_minutes,
         'location': m.location, 'notes': m.notes, 'status': m.status}
        for m in case.meetings.all()
    ]})


@csrf_exempt
@require_http_methods(["POST"])
def create_meeting(request, case_id):
    if not request.user.is_authenticated or not request.user.is_admin():
        return JsonResponse({'error': 'Forbidden'}, status=403)
    case = get_object_or_404(Case, pk=case_id)
    data = json.loads(request.body)
    m = Meeting.objects.create(
        case=case, title=data.get('title', 'Consultation'),
        meeting_type=data.get('meeting_type', Meeting.TYPE_ONLINE),
        scheduled_at=data['scheduled_at'],
        duration_minutes=data.get('duration_minutes', 60),
        location=data.get('location', ''), notes=data.get('notes', ''),
        created_by=request.user,
    )
    return JsonResponse({'id': m.pk, 'title': m.title, 'scheduled_at': m.scheduled_at.isoformat()}, status=201)


@csrf_exempt
@require_http_methods(["POST"])
def update_meeting(request, meeting_id):
    if not request.user.is_authenticated or not request.user.is_admin():
        return JsonResponse({'error': 'Forbidden'}, status=403)
    meeting = get_object_or_404(Meeting, pk=meeting_id)
    data = json.loads(request.body)
    for f in ('title', 'meeting_type', 'scheduled_at', 'duration_minutes', 'location', 'notes', 'status'):
        if f in data:
            setattr(meeting, f, data[f])
    meeting.save()
    return JsonResponse({'ok': True})
