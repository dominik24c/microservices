from dotenv import load_dotenv

from app.consumer import MessageBroker, callback


def main() -> None:
    load_dotenv()
    mb = MessageBroker('rabbitmq')
    mb.channel.basic_consume(queue='newsletter', on_message_callback=callback, auto_ack=True)
    mb.channel.start_consuming()

if __name__ == '__main__':
    main()
