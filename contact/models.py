import uuid
from django.db import models


class Request(models.Model):
    SOURCE_SITE = 'site'
    SOURCE_BOT = 'bot'
    SOURCES = [(SOURCE_SITE, 'Site'), (SOURCE_BOT, 'Telegram Bot')]

    STATUS_NEW = 'new'
    STATUS_REVIEWING = 'reviewing'
    STATUS_OFFERED = 'offered'
    STATUS_PAID = 'paid'
    STATUS_ASSIGNED = 'assigned'
    STATUS_CLOSED = 'closed'
    STATUSES = [
        (STATUS_NEW, 'New'),
        (STATUS_REVIEWING, 'Reviewing'),
        (STATUS_OFFERED, 'Offered'),
        (STATUS_PAID, 'Paid'),
        (STATUS_ASSIGNED, 'Assigned'),
        (STATUS_CLOSED, 'Closed'),
    ]

    DIRECTIONS = [
        ('family', 'Family'),
        ('criminal', 'Criminal'),
        ('labor', 'Labor'),
        ('tax', 'Tax'),
        ('contract', 'Contract'),
        ('other', 'Other'),
    ]

    customer_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    text = models.TextField()
    file = models.FileField(upload_to='requests/', blank=True, null=True)
    source = models.CharField(max_length=10, choices=SOURCES, default=SOURCE_SITE)
    telegram_chat_id = models.CharField(max_length=50, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUSES, default=STATUS_NEW)
    direction = models.CharField(max_length=20, choices=DIRECTIONS, blank=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    admin_comment = models.TextField(blank=True)
    # Secure token for client cabinet access — no login required
    access_token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    class Meta:
        ordering = ['-date']
        indexes = [
            models.Index(fields=['date']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"#{self.pk} {self.customer_name} - {self.status}"

    def minimum_payment(self):
        from decimal import Decimal
        if self.total_amount:
            return (self.total_amount * Decimal('10') / Decimal('100')).quantize(Decimal('0.01'))
        return None
