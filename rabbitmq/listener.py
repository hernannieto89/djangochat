#!/usr/bin/env python3
"""
RabbitMQ Bot
"""
import websocket
import pika
import csv
import requests
import json
import re

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='djangochat')


def callback(ch, method, properties, body):
    """
    Callback function for RabbitMQ handler.
    :param ch: _
    :param method: _
    :param properties: _
    :param body: String
    """
    print(" [x] Received %r" % body)

    msg, room = process_msg(body)

    ws = websocket.WebSocket()
    ws.connect(url="ws://127.0.0.1:8000/ws/chat/" + room + "/")
    ws.send(json.dumps({'message': msg}))
    ws.close()

    print("Sent: {}".format(msg))


def process_msg(body):
    """
    Processes message. Validates if given command exists.
    :param body: String
    :return: String
    """
    message = body.decode('utf-8')
    json_msg = json.loads(message)
    regex = re.compile('/stock=(.*)')
    match = regex.match(json_msg['message'])

    if match:
        stock_name = match.group().split('=')[1]
        if stock_name:
            return get_stock_info(stock_name), json_msg['room']
        else:
            return 'Parameter missing.', json_msg['room']
    else:
        return 'Invalid command.', json_msg['room']


def get_stock_info(stock_name):
    """
    Fetch stock information from endpoint.
    Creates string response.
    :param stock_name: String
    :return: String
    """
    endpoint = 'https://stooq.com/q/l/?s={}.us&f=sd2t2ohlcv&h&e=csv'.format(stock_name.lower())
    response = requests.get(endpoint)

    decoded_content = response.content.decode('utf-8')
    cr = list(csv.reader(decoded_content.splitlines(), delimiter=','))

    return "{0} quote is ${1} per share".format(stock_name, cr[1][6])


channel.basic_consume(callback,
                      queue='djangochat',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()









