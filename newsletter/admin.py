from django.contrib import admin
from .models import Message, Mailing, Recipient
from .utils import send_mailing


class RecipientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'description')
    search_fields = ('full_name', 'email')


class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject',)
    search_fields = ('subject',)


@admin.action(description='Отправить выбранные рассылки')
def send_selected_mailings(modeladmin, request, queryset):
    for mailing in queryset:
        try:
            send_mailing(mailing.id)
            modeladmin.message_user(request, f'Рассылка {mailing.id} отправлена')
        except Exception as e:
            modeladmin.message_user(request, f'Ошибка при отправке рассылки {mailing.id}: {str(e)}', level='ERROR')


class MailingAdmin(admin.ModelAdmin):
    list_display = ('message', 'first_sent_at', 'end_at', 'status')
    list_filter = ('status',)
    search_fields = ('message__subject',)


admin.site.register(Recipient, RecipientAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Mailing, MailingAdmin)
