#!/usr/bin/env python3

import websocket
import pika
import csv
import requests
import json

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='djangochat')


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

    msg = process_msg(body)

    ws = websocket.WebSocket()
    ws.connect(url="ws://127.0.0.1:8000/ws/chat/1/")
    ws.send(json.dumps({'message': msg}))
    ws.close()

    print("Sent: {}".format(msg))


def process_msg(body):
    body = body.decode('utf-8')
    if body == 'Invalid command.':
        return body
    return get_stock_info(body)


def get_stock_info(stock_name):

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









