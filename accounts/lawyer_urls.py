from django.urls import path
from . import views

urlpatterns = [
    path('', views.lawyer_office, name='lawyer_office'),
    path('case/<int:case_id>/', views.lawyer_case, name='lawyer_case'),
]
