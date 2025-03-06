from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings

User = get_user_model()


class Recipient(models.Model):
    email = models.EmailField(unique=True, verbose_name='Email')
    full_name = models.CharField(max_length=255, verbose_name='Ф.И.О.')
    description = models.TextField(blank=True, verbose_name='Комментарий')
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipients')

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Получатель"
        verbose_name_plural = "Получатели"


class Message(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"


class Mailing(models.Model):
    STATUS_CHOICES = [
        ('Создана', 'Создана'),
        ('Запущена', 'Запущена'),
        ('Завершена', 'Завершена'),
    ]

    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='Сообщение')
    recipients = models.ManyToManyField(Recipient, verbose_name='Получатели')
    first_sent_at = models.DateTimeField(verbose_name='Дата и время первой отправки')
    end_at = models.DateTimeField(verbose_name='Дата и время окончания отправки')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Создана', verbose_name='Статус')
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=False,
        verbose_name='Владелец'
    )

    def __str__(self):
        return f"Mailing {self.id} - {self.status}"

    def send_manual_mailing(self):
        recipients = self.recipients.all()
        for recipient in recipients:
            try:
                send_mail(
                    subject=self.message.subject,
                    message=self.message.body,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[recipient.email],
                    fail_silently=False,
                )
                MailingAttempt.objects.create(
                    mailing=self,
                    status='success',
                    server_response='Сообщение успешно отправлено',
                )
            except Exception as e:
                MailingAttempt.objects.create(
                    mailing=self,
                    status='failed',
                    server_response=str(e),
                )

    class Meta:
        permissions = [
            ("view_all_mailings", "Can view all mailings"),
            ("change_all_mailings", "Can change all mailings"),
        ]


class MailingAttempt(models.Model):
    SUCCESS = 'Успешно'
    FAILURE = 'Не успешно'
    STATUS_CHOICES = [
        (SUCCESS, 'Успешно'),
        (FAILURE, 'Не успешно'),
    ]

    attempt_datetime = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    server_response = models.TextField()
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name='attempts')

    def __str__(self):
        return f"Attempt {self.id} - {self.status}"
