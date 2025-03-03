from django.urls import reverse_lazy
from .models import  Message, Mailing, MailingAttempt, Recipient
from django.views.generic import ListView, TemplateView, UpdateView, DeleteView, CreateView, DetailView, View
from .forms import  MessageForm, MailingForm
from .forms import RecipientForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from .utils import send_mailing





# Главная страница
class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = 'newsletter/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_mailings'] = Mailing.objects.count()
        context['active_mailings'] = Mailing.objects.filter(status='Запущена').count()
        context['unique_recipients'] = Recipient.objects.values('email').distinct().count()
        context['recent_mailings'] = Mailing.objects.order_by('-updated_at')[:3]
        context['recent_messages'] = Message.objects.order_by('-updated_at')[:3]
        context['recent_recipients'] = Recipient.objects.order_by('-updated_at')[:3]
        return context


# Получатели рассылки
class RecipientListView(LoginRequiredMixin, ListView):
    model = Recipient
    template_name = 'newsletter/recipients_list.html'
    context_object_name = 'recipients'
    ordering = ['-updated_at']

    def get_queryset(self):
        if self.request.user.groups.filter(name='Менеджер').exists():
            return Recipient.objects.all()  # Менеджер видит всех получателей
        return Recipient.objects.filter(user=self.request.user)



class RecipientDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Recipient
    template_name = 'newsletter/recipients_detail.html'
    context_object_name = 'recipient'

    def test_func(self):
        recipient = self.get_object()
        if self.request.user.is_superuser or self.request.user.groups.filter(name='Менеджер').exists():
            return True
        return recipient.user == self.request.user

class RecipientCreateView(LoginRequiredMixin, CreateView):
    model = Recipient
    form_class = RecipientForm
    template_name = 'newsletter/recipients_form.html'
    success_url = reverse_lazy('newsletter:recipients_list')

    def form_valid(self, form):
        form.instance.user = self.request.user  # Привязываем получателя к текущему пользователю
        return super().form_valid(form)


class RecipientUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Recipient
    form_class = RecipientForm
    template_name = 'newsletter/recipients_form.html'
    success_url = reverse_lazy('newsletter:recipients_list')

    def test_func(self):
        recipient = self.get_object()
        # Только владелец получателя может его редактировать
        return recipient.user == self.request.user

class RecipientDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Recipient
    template_name = 'newsletter/recipients_confirm_delete.html'
    success_url = reverse_lazy('newsletter:recipients_list')

    def test_func(self):
        recipient = self.get_object()
        # Только владелец получателя может его удалить
        return recipient.user == self.request.user

#Сообщения
class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'newsletter/message_list.html'
    context_object_name = 'messages'
    ordering = ['-updated_at']  # Сортировка по полю updated_at в порядке убывания


class MessageDetailView(LoginRequiredMixin,DetailView):
    model = Message
    template_name = 'newsletter/message_detail.html'


class MessageCreateView(LoginRequiredMixin,CreateView):
    model = Message
    template_name = 'newsletter/message_form.html'
    form_class = MessageForm
    success_url = reverse_lazy('newsletter:message_list')


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    template_name = 'newsletter/message_form.html'
    fields = ['subject', 'body']
    success_url = reverse_lazy('newsletter:message_list')  # Исправлено

class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = 'newsletter/message_confirm_delete.html'
    success_url = reverse_lazy('newsletter:message_list')


#Рассылки
class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = 'newsletter/mailing_list.html'
    context_object_name = 'mailings'

    def get_queryset(self):
        if self.request.user.groups.filter(name='Менеджер').exists():
            return Mailing.objects.all()
        return Mailing.objects.filter(user=self.request.user)

class MailingDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Mailing
    template_name = 'newsletter/mailing_detail.html'
    context_object_name = 'mailing'

    def test_func(self):
        mailing = self.get_object()
        if self.request.user.groups.filter(name='Менеджер').exists():
            return True
        return mailing.user == self.request.user

class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'newsletter/mailing_form.html'
    success_url = reverse_lazy('newsletter:mailing_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class MailingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'newsletter/mailing_form.html'
    success_url = reverse_lazy('newsletter:mailing_list')  # Исправлено

    def test_func(self):
        mailing = self.get_object()
        if self.request.user.groups.filter(name='Менеджер').exists():
            return False  # Менеджеры не могут редактировать рассылки
        return mailing.user == self.request.user

class MailingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Mailing
    template_name = 'newsletter/mailing_confirm_delete.html'
    success_url = reverse_lazy('newsletter:mailing_list')  # Исправлено

    def test_func(self):
        mailing = self.get_object()
        if self.request.user.groups.filter(name='Менеджер').exists():
            return False  # Менеджеры не могут удалять рассылки
        return mailing.user == self.request.user

def send_mailing(mailing):
    recipients = mailing.recipients.all()
    subject = mailing.message.subject
    message = mailing.message.body
    from_email = 'YuKDj@yandex.ru'  # Замените на ваш email

    for recipient in recipients:
        try:
            send_mail(subject, message, from_email, [recipient.email])
            MailingAttempt.objects.create(
                mailing=mailing,
                status='Успешно',
                server_response='Письмо успешно отправлено'
            )
        except Exception as e:
            MailingAttempt.objects.create(
                mailing=mailing,
                status='Не успешно',
                server_response=str(e)
            )


def send_mailing_manually(request):
    if request.method == 'POST':
        mailing_id = request.POST.get('mailing_id')
        try:
            send_mailing(mailing_id)
            messages.success(request, 'Рассылка успешно отправлена!')  # Используем модуль messages
        except Exception as e:
            messages.error(request, f'Ошибка: {str(e)}')  # Используем модуль messages
        return redirect('newsletter:send_mailing_manually')

    # Получаем список всех сообщений и рассылок
    message_list = Message.objects.all()  # Переименовываем переменную
    mailings = Mailing.objects.all()
    return render(request, 'newsletter/send_mailing.html', {
        'messages': message_list,  # Передаем переименованную переменную в шаблон
        'mailings': mailings,
    })


class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    template_name = 'newsletter/user_list.html'
    context_object_name = 'users'

    def test_func(self):
        # Только менеджер может просматривать список пользователей
        return self.request.user.groups.filter(name='Менеджер').exists()


class BlockUserView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        # Только менеджер может блокировать пользователей
        return self.request.user.groups.filter(name='Менеджер').exists()

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.is_active = False
        user.save()
        return redirect('newsletter:user_list')

class DisableMailingView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        # Только менеджер может отключать рассылки
        return self.request.user.groups.filter(name='Менеджер').exists()

    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        mailing.is_active = False
        mailing.save()
        return redirect('newsletter:mailing_list')