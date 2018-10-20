import re
import requests
import csv
from chat.models import ChatMessage


def process_msg(message, user):

    response = None

    if message.startswith('/'):
        regex = re.compile('/stock=(.*)')
        match = regex.match(message)

        if match:
            stock = match.group().split('=')[1]

            response = get_stock_info(stock)
        else:
            response = 'Invalid command.'
    else:
        m = ChatMessage(user=user, message=str(user) + ': ' + message)
        m.save()

    return response


def get_stock_info(stock_name):

    endpoint = 'https://stooq.com/q/l/?s={}.us&f=sd2t2ohlcv&h&e=csv'.format(stock_name.lower())

    response = requests.get(endpoint)

    decoded_content = response.content.decode('utf-8')
    cr = list(csv.reader(decoded_content.splitlines(), delimiter=','))

    return "{0} quote is ${1} per share".format(stock_name, cr[1][6])

