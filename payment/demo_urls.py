from django.urls import path
from .demo_views import demo_pay

urlpatterns = [
    path('pay/<int:invoice_id>/<str:method>/', demo_pay, name='demo_pay'),
]
