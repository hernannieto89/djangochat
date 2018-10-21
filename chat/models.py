# chat/models.py
"""
Models for Chat App - DjangoChat project.
"""
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class ChatMessage(models.Model):
    """
    Model to represent user message
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(max_length=3000)
    room = models.CharField(max_length=100, null=False, default='lobby')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        String to represent the message
        """
        return self.message


class Profile(models.Model):
    """
    Model to represent user profile
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(null=True, blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Creates user profile on user creation.
    :param sender: _
    :param instance: User instance
    :param created: Created flag
    :param kwargs: _
    """
    if created:
        Profile.objects.create(user=instance)
