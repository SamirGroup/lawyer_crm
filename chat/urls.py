from django.urls import path
from . import views

urlpatterns = [
    path('send/', views.send_message, name='api_send_message'),
    path('pre/', views.get_pre_messages, name='api_pre_messages'),
    path('<int:case_id>/', views.get_messages, name='api_get_messages'),
    path('<int:case_id>/monitor/', views.admin_monitor_chat, name='api_admin_monitor'),
    path('<int:case_id>/status/', views.update_case_status, name='api_update_case_status'),
    path('<int:case_id>/meetings/', views.get_meetings, name='api_get_meetings'),
    path('<int:case_id>/meetings/create/', views.create_meeting, name='api_create_meeting'),
    path('meeting/<int:meeting_id>/update/', views.update_meeting, name='api_update_meeting'),
]
