from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_ADMIN = 'admin'
    ROLE_LAWYER = 'lawyer'
    ROLES = [(ROLE_ADMIN, 'Admin'), (ROLE_LAWYER, 'Lawyer')]

    role = models.CharField(max_length=10, choices=ROLES, default=ROLE_LAWYER)
    phone = models.CharField(max_length=20, blank=True)

    def is_admin(self):
        return self.role == self.ROLE_ADMIN

    def is_lawyer(self):
        return self.role == self.ROLE_LAWYER


class Lawyer(models.Model):
    DIRECTIONS = [
        ('family', 'Family'),
        ('criminal', 'Criminal'),
        ('labor', 'Labor'),
        ('tax', 'Tax'),
        ('contract', 'Contract'),
        ('other', 'Other'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='lawyer_profile')
    direction = models.CharField(max_length=20, choices=DIRECTIONS)
    phone = models.CharField(max_length=20, blank=True)
    telegram_id = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.direction})"
