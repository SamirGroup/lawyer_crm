from django.db import models


class Case(models.Model):
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_DOC_READY = 'doc_ready'
    STATUS_COMPLETED = 'completed'
    STATUSES = [
        (STATUS_IN_PROGRESS, 'In Progress'),
        (STATUS_DOC_READY, 'Document Ready'),
        (STATUS_COMPLETED, 'Completed'),
    ]

    request = models.OneToOneField('contact.Request', on_delete=models.CASCADE, related_name='case')
    lawyer = models.ForeignKey('accounts.Lawyer', on_delete=models.SET_NULL, null=True, related_name='cases')
    attached_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUSES, default=STATUS_IN_PROGRESS)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Case #{self.request_id} — {self.lawyer}"


class Message(models.Model):
    SENDER_CLIENT = 'client'
    SENDER_LAWYER = 'lawyer'
    SENDER_ADMIN = 'admin'
    SENDERS = [
        (SENDER_CLIENT, 'Client'),
        (SENDER_LAWYER, 'Lawyer'),
        (SENDER_ADMIN, 'Admin'),
    ]

    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=10, choices=SENDERS)
    sender_name = models.CharField(max_length=100, blank=True)
    text = models.TextField(blank=True)
    file = models.FileField(upload_to='chat_files/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"[{self.sender}] {self.text[:50]}"


class PreCaseMessage(models.Model):
    """Client messages sent before a case/lawyer is assigned."""
    request = models.ForeignKey('contact.Request', on_delete=models.CASCADE, related_name='pre_messages')
    text = models.TextField(blank=True)
    file = models.FileField(upload_to='chat_files/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"[pre #{self.request_id}] {self.text[:50]}"


class Meeting(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_CONFIRMED = 'confirmed'
    STATUS_CANCELLED = 'cancelled'
    STATUS_DONE = 'done'
    STATUSES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_CONFIRMED, 'Confirmed'),
        (STATUS_CANCELLED, 'Cancelled'),
        (STATUS_DONE, 'Done'),
    ]
    TYPE_ONLINE = 'online'
    TYPE_OFFICE = 'office'
    TYPES = [(TYPE_ONLINE, 'Online'), (TYPE_OFFICE, 'In Office')]

    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='meetings')
    title = models.CharField(max_length=200)
    meeting_type = models.CharField(max_length=10, choices=TYPES, default=TYPE_ONLINE)
    scheduled_at = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField(default=60)
    location = models.CharField(max_length=300, blank=True)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=15, choices=STATUSES, default=STATUS_PENDING)
    created_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['scheduled_at']

    def __str__(self):
        return f"{self.title} — {self.scheduled_at.strftime('%d.%m.%Y %H:%M')}"
