from django.db import models
from django.utils import timezone


class Invoice(models.Model):
    request = models.OneToOneField('contact.Request', on_delete=models.CASCADE, related_name='invoice')
    invoice_number = models.CharField(max_length=30, unique=True)
    ten_percent_amount = models.DecimalField(max_digits=12, decimal_places=2)
    paid = models.BooleanField(default=False)
    paid_date = models.DateTimeField(null=True, blank=True)
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    payment_method = models.CharField(max_length=10, blank=True)  # payme / click
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=['invoice_number'])]

    def __str__(self):
        return self.invoice_number

    @classmethod
    def generate_number(cls):
        today = timezone.now().strftime('%Y%m%d')
        last = cls.objects.filter(invoice_number__startswith=f'INV-{today}').count()
        return f"INV-{today}-{str(last + 1).zfill(4)}"
