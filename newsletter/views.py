from django.urls import reverse_lazy
from .models import Recipient, Message
from django.views.generic import ListView, TemplateView, UpdateView, DeleteView, CreateView, DetailView
from .forms import RecipientForm, MessageForm


# Главная страница
class HomePageView(TemplateView):
    template_name = 'newsletter/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_recipients'] = Recipient.objects.order_by('-updated_at')[:3]
        context['recent_messages'] = Message.objects.order_by('-updated_at')[:3]  # Последние три сообщения

        return context

    def home(request):

        total_mailings = Mailing.objects.count()
        active_mailings = Mailing.objects.filter(status='Запущена').count()
        unique_recipients = Recipient.objects.values('email').distinct().count()

        recent_mailings = Mailing.objects.order_by('-updated_at')[:3]
        recent_messages = Message.objects.order_by('-updated_at')[:3]  # Предполагается, что у вас есть модель Message
        recent_recipients = Recipient.objects.order_by('-updated_at')[:3]

        context = {
           'total_mailings': total_mailings,
           'active_mailings': active_mailings,
           'unique_recipients': unique_recipients,
           'recent_mailings': recent_mailings,
           'recent_messages': recent_messages,
           'recent_recipients': recent_recipients,
        }
        return render(request, 'newsletter/home.html', context)



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