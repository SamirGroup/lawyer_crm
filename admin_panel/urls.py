from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='admin_dashboard'),
    path('requests/', views.requests_list, name='admin_requests'),
    path('requests/<int:pk>/', views.request_detail, name='admin_request_detail'),
    path('requests/<int:pk>/update/', views.update_request, name='admin_update_request'),
    path('requests/<int:pk>/invoice/', views.create_invoice_admin, name='admin_create_invoice'),
    path('requests/<int:pk>/assign/', views.assign_lawyer, name='admin_assign_lawyer'),
    path('lawyers/', views.lawyers_list, name='admin_lawyers'),
    path('lawyers/add/', views.add_lawyer, name='admin_add_lawyer'),
    path('lawyers/<int:pk>/delete/', views.delete_lawyer, name='admin_delete_lawyer'),
]
