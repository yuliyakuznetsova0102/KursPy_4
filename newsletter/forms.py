from django import forms
from .models import Recipient


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
