# chat/models.py
"""
Models for Chat App - DjangoChat project.
"""
from django.db import models
from django.contrib.auth.models import User


class ChatMessage(models.Model):
    """
    Model to represent user message
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(max_length=3000)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        String to represent the message
        """
        return self.message
