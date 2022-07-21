import json

import pika
from pika.adapters.blocking_connection import BlockingChannel

from .mail import send_email


class MessageBroker:
    def __init__(self, host: str, hb:int=600, bct:int=300) -> None:
        parameters = pika.ConnectionParameters(host=host, heartbeat=hb, blocked_connection_timeout=bct)
        self.__connection = pika.BlockingConnection(parameters)
        self.__channel = self.__connection.channel()
        self.__channel.queue_declare(queue='newsletter')

    @property
    def channel(self) -> BlockingChannel:
        return self.__channel
    

def callback(ch, method, properties, body) -> None:
    data = json.loads(body)
    if properties.content_type == 'send_newsletter':
        send_email('Newsletter of Game Ratings Service', 'We sent newsletter to you!', data['email'])
