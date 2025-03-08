from django import forms
from .models import Message, Mailing
from .models import Recipient


class RecipientForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = ['full_name', 'email', 'description']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Введите email'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите Ф.И.О.'}),
        }
        labels = {
            'full_name': 'Ф.И.О.',
            'email': 'Email',
        }

        def form_valid(self, form):
            print(form.errors)
            return super().form_valid(form)


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите тему письма'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Введите текст письма', 'rows': 6}),
        }
        labels = {
            'subject': 'Тема письма',
            'body': 'Тело письма',
        }

    def form_valid(self, form):
        print(form.errors)
        return super().form_valid(form)


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ['first_sent_at', 'end_at', 'status', 'message', 'recipients']

    def __init__(self, *args, **kwargs):
        owner = kwargs.pop('owner', None)
        super(MailingForm, self).__init__(*args, **kwargs)

        if owner:
            self.fields['message'].queryset = Message.objects.filter(owner=owner)
            self.fields['recipients'].queryset = Recipient.objects.filter(owner=owner)

    def form_valid(self, form):
        print(form.errors)
        return super().form_valid(form)
