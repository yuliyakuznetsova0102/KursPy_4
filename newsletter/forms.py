from django import forms
from .models import Recipient, Message, Mailing


class RecipientForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = ['full_name', 'email', 'description']  # исправлено с 'name' на 'full_name'
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Введите email'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите Ф.И.О.'}),
            # добавлено поле для Ф.И.О.
        }
        labels = {
            'full_name': 'Ф.И.О.',  # исправлено с 'name' на 'full_name'
            'email': 'Email',
        }

        def form_valid(self, form):
            print(form.errors)  # Выводим ошибки формы в консоль
            return super().form_valid(form)


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body']  # Указываем поля для формы
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите тему письма'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Введите текст письма', 'rows': 6}),
        }
        labels = {
            'subject': 'Тема письма',
            'body': 'Тело письма',
        }

    def form_valid(self, form):
        print(form.errors)  # Выводим ошибки формы в консоль
        return super().form_valid(form)


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ['message', 'first_sent_at', 'end_at', 'status', 'recipients']  # Указываем поля для формы
        widgets = {
            'first_sent_at': forms.DateTimeInput(
                attrs={'class': 'form-control', 'placeholder': 'Дата и время первой отправки'}),
            'end_at': forms.DateTimeInput(
                attrs={'class': 'form-control', 'placeholder': 'Дата и время окончания отправки'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'message': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Введите текст сообщения', 'rows': 6}),
            'recipients': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите получателей'}),
        }


    def form_valid(self, form):
        print(form.errors)  # Выводим ошибки формы в консоль
        return super().form_valid(form)