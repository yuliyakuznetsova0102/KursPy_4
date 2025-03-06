from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('user', 'Пользователь'),
        ('manager', 'Менеджер'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        permissions = [
            ("can_view_all_mailings", "Can view all mailings"),
            ("can_view_all_users", "Can view all recipients"),
            ("can_block_users", "Can block users"),
            ("can_disable_mailings", "Can disable mailings"),
        ]
