from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/', views.get_invoice, name='api_get_invoice'),
    path('create/<int:pk>/', views.create_invoice, name='api_create_invoice'),
]
