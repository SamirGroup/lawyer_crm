from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('status/', views.status_page, name='status'),
    path('payment/', views.payment_bare, name='payment_bare'),
    path('payment/<int:pk>/', views.payment_page, name='payment'),
    path('cabinet/', views.cabinet_bare, name='cabinet_bare'),
    path('cabinet/<uuid:token>/', views.cabinet, name='cabinet'),
]
