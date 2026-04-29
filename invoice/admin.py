from django.contrib import admin
from .models import Invoice


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'request', 'ten_percent_amount', 'paid', 'paid_date')
    list_filter = ('paid',)
