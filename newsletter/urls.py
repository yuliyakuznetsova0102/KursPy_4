from django.urls import path
from .views import (
    HomePageView,
    RecipientListView, RecipientCreateView, RecipientUpdateView, RecipientDeleteView, RecipientDetailView,
    MessageListView, MessageDetailView, MessageCreateView, MessageUpdateView, MessageDeleteView,
)

urlpatterns = [
    path('home/', HomePageView.as_view(), name='home'),
    path('recipients_list/', RecipientListView.as_view(), name='recipients_list'),
    path('recipients_detail/<int:pk>/', RecipientDetailView.as_view(), name='recipients_detail'),
    path('recipients/create/', RecipientCreateView.as_view(), name='recipients_create'),
    path('recipients/update/<int:pk>/', RecipientUpdateView.as_view(), name='recipients_update'),
    path('recipients/delete/<int:pk>/', RecipientDeleteView.as_view(), name='recipients_delete'),

    path('message_list/', MessageListView.as_view(), name='message_list'),
    path('message_detail/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('message/create/', MessageCreateView.as_view(), name='message_create'),
    path('message/update/<int:pk>/', MessageUpdateView.as_view(), name='message_update'),
    path('message/delete/<int:pk>/', MessageDeleteView.as_view(), name='message_delete'),
]
