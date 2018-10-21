import re
import pika
from chat.models import ChatMessage

from django.contrib.auth.models import AnonymousUser


def process_msg(message, user):

    if message.startswith('/'):
        regex = re.compile('/stock=(.*)')
        match = regex.match(message)

        if match:
            msg = match.group().split('=')[1]
        else:
            msg = 'Invalid command.'

        publish_request(msg)

    else:
        m = ChatMessage(user=user, message=str(user) + ': ' + message)
        m.save()


def publish_request(response):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

    channel = connection.channel()
    channel.queue_declare(queue='djangochat')
    channel.basic_publish(exchange='',
                          routing_key='djangochat',
                          body=response)
    connection.close()


def user_sanitizer(user):
    if isinstance(user, AnonymousUser):
        return 'Bot'
    else:
        return str(user)
