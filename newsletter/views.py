from django.urls import reverse_lazy, reverse

from .models import Message, Mailing, MailingAttempt, Recipient
from django.views.generic import ListView, TemplateView, UpdateView, DeleteView, CreateView, DetailView, View
from .forms import MessageForm, MailingForm
from .forms import RecipientForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.db.models import Count, Q
from users.models import CustomUser




# Главная страница
class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = 'newsletter/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context['total_mailings'] = Mailing.objects.filter(owner=user).count()
        context['active_mailings'] = Mailing.objects.filter(owner=user, status='Запущена').count()
        context['unique_recipients'] = Recipient.objects.filter(owner=user).values('email').distinct().count()

        # Последние три записи для каждого типа данных
        context['recent_mailings'] = Mailing.objects.filter(owner=user).order_by('-updated_at')[:3]
        context['recent_messages'] = Message.objects.filter(owner=user).order_by('-updated_at')[:3]
        context['recent_recipients'] = Recipient.objects.filter(owner=user).order_by('-updated_at')[:3]

        return context


# Получатели рассылки
class RecipientListView(LoginRequiredMixin, ListView):
    model = Recipient
    template_name = 'newsletter/recipients_list.html'
    context_object_name = 'recipients'
    ordering = ['-updated_at']

    def get_queryset(self):
        if self.request.user.role == 'manager':
            return Recipient.objects.all()
        return Recipient.objects.filter(owner=self.request.user)


class RecipientDetailView(LoginRequiredMixin, DetailView):
    model = Recipient
    template_name = 'newsletter/recipients_detail.html'
    context_object_name = 'recipient'

    def get_queryset(self):
        return Recipient.objects.filter(owner=self.request.user)


class RecipientCreateView(LoginRequiredMixin, CreateView):
    model = Recipient
    form_class = RecipientForm
    template_name = 'newsletter/recipients_form.html'
    success_url = reverse_lazy('newsletter:recipients_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class RecipientUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipient
    form_class = RecipientForm
    template_name = 'newsletter/recipients_form.html'
    success_url = reverse_lazy('newsletter:recipients_list')

    def get_queryset(self):
        return Recipient.objects.filter(owner=self.request.user) or self.request.user.role == 'manager'


class RecipientDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipient
    template_name = 'newsletter/recipients_confirm_delete.html'
    success_url = reverse_lazy('newsletter:recipients_list')

    def test_func(self):
        recipient = self.get_object()
        return recipient.owner == self.request.user


# Сообщения
class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'newsletter/message_list.html'
    context_object_name = 'messages'
    ordering = ['-updated_at']

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)


def get_queryset(self):
    return Message.objects.filter(owner=self.request.user)


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = 'newsletter/message_detail.html'


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    template_name = 'newsletter/message_form.html'
    form_class = MessageForm
    success_url = reverse_lazy('newsletter:message_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    template_name = 'newsletter/message_form.html'
    fields = ['subject', 'body']
    success_url = reverse_lazy('newsletter:message_list')

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = 'newsletter/message_confirm_delete.html'
    success_url = reverse_lazy('newsletter:message_list')

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)


# Рассылки
class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = 'newsletter/mailing_list.html'
    context_object_name = 'mailings'

    def get_queryset(self):
        if self.request.user.role == 'manager':
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=self.request.user)


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = 'newsletter/mailing_detail.html'
    context_object_name = 'mailing'

    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user)

    def post(self, request, *args, **kwargs):
        mailing = self.get_object()
        mailing.send_manual_mailing()
        return redirect(reverse('newsletter:mailing_detail', kwargs={'pk': mailing.pk}))


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'newsletter/mailing_form.html'
    success_url = reverse_lazy('newsletter:mailing_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['owner'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'newsletter/mailing_form.html'
    success_url = reverse_lazy('newsletter:mailing_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['owner'] = self.request.user
        return kwargs

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    template_name = 'newsletter/mailing_confirm_delete.html'
    success_url = reverse_lazy('newsletter:mailing_list')

    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user)


class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = CustomUser
    template_name = 'mailing/user_list.html'
    context_object_name = 'users'

    def test_func(self):
        return self.request.user.role == 'manager'


class MailingStatsView(ListView):
    model = Mailing
    template_name = 'newsletter/mailing_stats.html'
    context_object_name = 'mailings'

    def get_queryset(self):
        user = self.request.user

        return Mailing.objects.filter(owner=user).annotate(
            total_attempts=Count('attempts'),
            successful_attempts=Count('attempts', filter=Q(attempts__status='success')),
            failed_attempts=Count('attempts', filter=Q(attempts__status='failed'))
        )


class MailingAttemptListView(ListView):
    model = MailingAttempt
    template_name = 'mailing_attempt_list.html'
    context_object_name = 'attempts'

    def get_queryset(self):
        user = self.request.user
        return MailingAttempt.objects.filter(mailing__owner=user)
