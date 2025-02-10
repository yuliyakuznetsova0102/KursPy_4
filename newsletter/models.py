from django.db import models
from django.utils import timezone

class Recipient(models.Model):
    email = models.EmailField(unique=True, verbose_name='Email')
    full_name = models.CharField(max_length=255, verbose_name='Ф.И.О.')
    description = models.TextField(blank=True, verbose_name='Комментарий')
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.full_name


class Message(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject



class Mailing(models.Model):
    STATUS_CHOICES = [
        ('Создана', 'Создана'),
        ('Запущена', 'Запущена'),
        ('Завершена', 'Завершена'),
    ]

    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    recipients = models.ManyToManyField(Recipient)
    first_sent_at = models.DateTimeField(default=timezone.now)
    end_at = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Создана')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Рассылка: {self.message.subject} ({self.status})"