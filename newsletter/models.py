from django.db import models

class Recipient(models.Model):
    email = models.EmailField(unique=True, verbose_name='Email')
    full_name = models.CharField(max_length=255, verbose_name='Ф.И.О.')
    description = models.TextField(blank=True, verbose_name='Комментарий')

    def __str__(self):
        return self.full_name


class Message(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()

    def __str__(self):
        return self.subject