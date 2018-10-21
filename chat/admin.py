# chat/admin
"""
Admin configuration for Chat App- DjangoChat project.
"""
from django.contrib import admin
from chat.models import ChatMessage, Profile

admin.site.register(ChatMessage)
admin.site.register(Profile)
