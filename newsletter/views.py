from django.urls import reverse_lazy
from .models import Recipient, Message
from django.views.generic import ListView, TemplateView, UpdateView, DeleteView, CreateView, DetailView
from .forms import RecipientForm



# Главная страница
class HomePageView(TemplateView):
    template_name = 'newsletter/home.html'

# Получатели рассылки
class RecipientListView(ListView):
    model = Recipient
    template_name = 'newsletter/recipients_list.html'
    context_object_name = 'recipients'

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
    template_name = 'message_list.html'

class MessageDetailView(DetailView):
    model = Message
    template_name = 'message_detail.html'

class MessageCreateView(CreateView):
    model = Message
    template_name = 'message_form.html'
    fields = ['subject', 'body']
    success_url = reverse_lazy('message_list')

class MessageUpdateView(UpdateView):
    model = Message
    template_name = 'message_form.html'
    fields = ['subject', 'body']
    success_url = reverse_lazy('message_list')

class MessageDeleteView(DeleteView):
    model = Message
    template_name = 'message_confirm_delete.html'
    success_url = reverse_lazy('message_list')