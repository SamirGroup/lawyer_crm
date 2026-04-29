from django.contrib import admin
from .models import Request


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('pk', 'customer_name', 'phone', 'source', 'status', 'date')
    list_filter = ('status', 'source', 'direction')
    search_fields = ('customer_name', 'phone')
