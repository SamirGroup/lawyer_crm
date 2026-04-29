from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

handler404 = 'law_crm.views.handler404'

urlpatterns = [
    path('', include('contact.urls')),
    path('accounts/', include('accounts.urls')),
    path('admin-panel/', include('admin_panel.urls')),
    path('lawyer/', include('accounts.lawyer_urls')),
    path('api/', include('contact.api_urls')),
    path('api/invoice/', include('invoice.urls')),
    path('api/payment/', include('payment.urls')),
    path('api/chat/', include('chat.urls')),
    path('bot/', include('bot.urls')),
    path('demo/', include('payment.demo_urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
