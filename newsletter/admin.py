from django.contrib import admin
from .models import Recipient, Message, Mailing

class RecipientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'description')
    search_fields = ('full_name', 'email')


class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject',)
    search_fields = ('subject',)


class MailingAdmin(admin.ModelAdmin):
    list_display = ('message', 'first_sent_at', 'end_at', 'status')
    list_filter = ('status',)
    search_fields = ('message__subject',)



admin.site.register(Recipient, RecipientAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Mailing, MailingAdmin)