# chat/utils.py
"""
Utilities module for Chat App - DjangoChat project.
"""
import pika
import json
from chat.models import ChatMessage

from django.contrib.auth.models import AnonymousUser


def get_last_messages(room_name):
    """
    Gets last 50 messages from the Database.
    Creates a string with all the messages appended.
    :param room_name: String
    :return: String
    """
    chat_queryset = ChatMessage.objects.filter(room=room_name).order_by("-created")[:50]
    chat_messages = reversed(chat_queryset)

    messages_raw = ''
    for message in chat_messages:
        messages_raw += message.message + '\n'

    return messages_raw


def process_msg(message, user, room_name):
    """
    Process chat message, if message starts with dash symbol it is handled to RabbitMQ Bot.
    If it is a regular message, it is stored in the DB.
    :param message: String
    :param room_name: String
    :param user: LazyObject
    """
    if message.startswith('/'):
        publish_request(json.dumps({'message': message, 'room': room_name}))
    else:
        m = ChatMessage(user=user, message=str(user) + ': ' + message, room=room_name)
        m.save()


def publish_request(message):
    """
    Publishes message to RabbitMQ server.
    :param message:
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

    channel = connection.channel()
    channel.queue_declare(queue='djangochat')
    channel.basic_publish(exchange='',
                          routing_key='djangochat',
                          body=message)
    connection.close()


def user_sanitizer(user):
    """
    Sanitizes username.
    :param user: User instance
    :return: String
    """
    if isinstance(user, AnonymousUser):
        return 'Bot'
    else:
        return str(user)
