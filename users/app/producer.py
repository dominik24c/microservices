import pika
import json


class MessageBroker:
    def __init__(self, host: str, hb:int=600, bct:int=300) -> None:
        parameters = pika.ConnectionParameters(host=host, heartbeat=hb, blocked_connection_timeout=bct)
        self.__connection = pika.BlockingConnection(parameters)
        self.__channel = self.__connection.channel()
    
    def publish(self, method: str, body: dict) -> None:
        data = json.dumps(body)
        properties = pika.BasicProperties(method)
        self.__channel.basic_publish(exchange='', routing_key='newsletter',body=data, properties=properties)

mb = MessageBroker('rabbitmq')
