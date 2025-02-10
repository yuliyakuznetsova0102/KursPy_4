from django.contrib import admin
from .models import Recipient, Message

class RecipientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'description')
    search_fields = ('full_name', 'email')


class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject',)
    search_fields = ('subject',)


admin.site.register(Recipient, RecipientAdmin)
admin.site.register(Message, MessageAdmin)
