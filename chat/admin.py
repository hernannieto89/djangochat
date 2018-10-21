# chat/admin
"""
Admin configuration for Chat App- DjangoChat project.
"""
from django.contrib import admin
from chat.models import ChatMessage

admin.site.register(ChatMessage)
