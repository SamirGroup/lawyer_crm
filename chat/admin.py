from django.contrib import admin
from .models import Case, Message, Meeting


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ('pk', 'request', 'lawyer', 'status', 'attached_date')
    list_filter = ('status',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('pk', 'case', 'sender', 'text', 'timestamp')


@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ('title', 'case', 'meeting_type', 'scheduled_at', 'status')
    list_filter = ('status', 'meeting_type')
