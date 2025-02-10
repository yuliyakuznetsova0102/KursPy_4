from django.urls import reverse_lazy
from .models import Recipient, Message, Mailing
from django.views.generic import ListView, TemplateView, UpdateView, DeleteView, CreateView, DetailView
from .forms import RecipientForm, MessageForm, MailingForm


# Главная страница
class HomePageView(TemplateView):
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
class RecipientListView(ListView):
    model = Recipient
    template_name = 'newsletter/recipients_list.html'
    context_object_name = 'recipients'
    ordering = ['-updated_at']  # Сортировка по полю updated_at в порядке убывания

    def get_queryset(self):
        # Можно дополнительно переопределить метод, если нужно что-то добавить в запрос
        return super().get_queryset()


class RecipientDetailView(DetailView):
    model = Recipient
    template_name = 'newsletter/recipients_detail.html'
    context_object_name = 'recipient'


class RecipientCreateView(CreateView):
    model = Recipient
    form_class = RecipientForm
    template_name = 'newsletter/recipients_form.html'
    success_url = reverse_lazy('recipients_list')


class RecipientUpdateView(UpdateView):
    model = Recipient
    form_class = RecipientForm
    template_name = 'newsletter/recipients_form.html'
    success_url = reverse_lazy('recipients_list')


class RecipientDeleteView(DeleteView):
    model = Recipient
    template_name = 'newsletter/recipients_confirm_delete.html'
    success_url = reverse_lazy('recipients_list')


#Сообщения
class MessageListView(ListView):
    model = Message
    template_name = 'newsletter/message_list.html'
    context_object_name = 'messages'
    ordering = ['-updated_at']  # Сортировка по полю updated_at в порядке убывания


class MessageDetailView(DetailView):
    model = Message
    template_name = 'newsletter/message_detail.html'


class MessageCreateView(CreateView):
    model = Message
    template_name = 'newsletter/message_form.html'
    form_class = MessageForm
    success_url = reverse_lazy('message_list')


class MessageUpdateView(UpdateView):
    model = Message
    template_name = 'newsletter/message_form.html'
    fields = ['subject', 'body']
    success_url = reverse_lazy('message_list')


class MessageDeleteView(DeleteView):
    model = Message
    template_name = 'newsletter/message_confirm_delete.html'
    success_url = reverse_lazy('message_list')


#Рассылки
class MailingListView(ListView):
    model = Mailing
    template_name = 'newsletter/mailing_list.html'
    context_object_name = 'mailings'

class MailingDetailView(DetailView):
    model = Mailing
    template_name = 'newsletter/mailing_detail.html'
    context_object_name = 'mailing'

class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'newsletter/mailing_form.html'
    success_url = reverse_lazy('mailing_list')

class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'newsletter/mailing_form.html'
    success_url = reverse_lazy('mailing_list')

class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = 'newsletter/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailing_list')