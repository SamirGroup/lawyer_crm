from django.urls import path
from . import views

urlpatterns = [
    path('payme/webhook/', views.payme_webhook, name='payme_webhook'),
    path('click/webhook/', views.click_webhook, name='click_webhook'),
]
