import json
import asyncio
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings


@csrf_exempt
@require_http_methods(["POST"])
def webhook(request):
    if not settings.TELEGRAM_BOT_TOKEN or settings.TELEGRAM_BOT_TOKEN == 'DEMO_NO_TOKEN':
        return JsonResponse({'error': 'Bot token not configured'}, status=503)

    from telegram import Update
    from .bot import build_application

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponse('bad request', status=400)

    app = build_application(settings.TELEGRAM_BOT_TOKEN)

    async def process():
        await app.initialize()
        update = Update.de_json(data, app.bot)
        await app.process_update(update)
        await app.shutdown()

    # Use a new event loop to avoid "loop already running" on Windows
    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(process())
    finally:
        loop.close()

    return HttpResponse('ok')
