from django.urls import path
from . import views

urlpatterns = [
    path('application/create/', views.create_request, name='api_create_request'),
    path('application/<int:pk>/', views.get_request, name='api_get_request'),
]
