from django.contrib import admin

from .models import Client, MailList, Tag, OperatorCode, Message

admin.site.register(Client)
admin.site.register(MailList)
admin.site.register(OperatorCode)
admin.site.register(Tag)
admin.site.register(Message)
