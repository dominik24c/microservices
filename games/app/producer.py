import json

import pika

class MessageBroker:
    def __init__(self, host: str, hb:int=600, bct:int=300) -> None:
        parameters = pika.ConnectionParameters(host=host, heartbeat=hb, blocked_connection_timeout=bct)
        self.__connection =  pika.BlockingConnection(parameters=parameters)
        self.__channel = self.__connection.channel()

    def pubish(self, method: str, body: dict) -> None:
        data = json.dumps(body)
        properties = pika.BasicProperties(method)
        self.__channel.basic_publish(exchange='', routing_key='games_ratings', body=data, properties=properties)

mb = MessageBroker('rabbitmq')
