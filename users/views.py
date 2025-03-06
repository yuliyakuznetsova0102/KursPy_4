from django.contrib.auth.views import (
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
)
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, View, FormView, DetailView, UpdateView
from django.contrib.auth import login, logout
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from newsletter.models import Recipient, Mailing
from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm
from .models import CustomUser
from .tokens import account_activation_token
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect




class UserRegistrationView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('newsletter:home')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        print(f"Пользователь создан: {user.username}, ID: {user.id}")

        self.send_confirmation_email(user)
        return super().form_valid(form)

    def send_confirmation_email(self, user):
        token = account_activation_token.make_token(user)
        print(f"Токен для пользователя {user.username}: {token}")

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        print(f"UID: {uid}, User ID: {user.pk}")

        confirmation_url = self.request.build_absolute_uri(
            reverse('users:confirm_email', kwargs={'uidb64': uid, 'token': token})
        )
        print(f"Ссылка для подтверждения: {confirmation_url}")

        subject = 'Подтвердите ваш email'
        message = f'Для подтверждения email перейдите по ссылке: {confirmation_url}'
        send_mail(subject, message, 'YuKDj@yandex.ru', [user.email])


class ConfirmEmailView(View):
    def get(self, request, uidb64, token):
        try:

            uid = force_str(urlsafe_base64_decode(uidb64))
            print(f"Decoded UID: {uid}")

            user = CustomUser.objects.get(pk=uid)
            print(f"Пользователь найден: {user.username}, ID: {user.id}")
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist) as e:
            user = None
            print(f"Ошибка: {e}")

        if user is not None:
            is_token_valid = account_activation_token.check_token(user, token)
            print(f"Проверка токена: {is_token_valid}")

            if is_token_valid:
                print("Токен действителен")
                user.is_active = True
                user.save()

                login(request, user)

                subject = 'Благодарим за регистрацию'
                message = 'Спасибо за регистрацию на нашем сервисе!'
                send_mail(subject, message, 'YuKDj@yandex.ru', [user.email])

                return redirect('newsletter:home')
            else:
                print("Токен недействителен")
        else:
            print("Пользователь не найден")

        return render(request, 'users/invalid_token.html')


class UserLoginView(FormView):
    form_class = UserLoginForm
    template_name = 'users/login.html'
    success_url = reverse_lazy('newsletter:home')

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return super().form_valid(form)

    def form_invalid(self, form):
        failed_attempts = self.request.session.get('failed_attempts', 0)
        failed_attempts += 1
        self.request.session['failed_attempts'] = failed_attempts

        if failed_attempts >= 3:
            form.add_error(None, "Вы ввели неправильный пароль 3 раза. Восстановите пароль.")
            self.request.session['failed_attempts'] = 0
        return super().form_invalid(form)


def user_logout(request):
    logout(request)
    return redirect('newsletter:home')


class UserPasswordResetView(PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'  # Шаблон письма
    success_url = reverse_lazy('users:password_reset_done')


class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('users:password_reset_complete')


class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'


class ProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'users/profile.html'
    context_object_name = 'user'

    def get_object(self):
        return self.request.user


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = UserProfileForm
    template_name = 'users/profile_edit.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self):
        return self.request.user


class BlockUserView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.role == 'manager'

    def get(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        user.is_active = False
        user.save()
        return redirect('user_list')
