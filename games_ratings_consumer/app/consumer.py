import json
import pika
from pika.adapters.blocking_connection import BlockingChannel

from .content_type import CreateGameRatings, DeleteGameRatings


class MessageBroker:
    def __init__(self, host: str) -> None:
        parameters = pika.ConnectionParameters(host=host)
        self.__connection = pika.BlockingConnection(parameters=parameters)
        self.__channel =  self.__connection.channel()
        self.__channel.queue_declare('games_ratings')
    
    @property
    def channel(self) -> BlockingChannel:
        return self.__channel


def callback(ch, method, properties, body) -> None:
    body = json.loads(body)
    handler = CreateGameRatings(DeleteGameRatings(None))
    handler.handle(properties.content_type, body)
