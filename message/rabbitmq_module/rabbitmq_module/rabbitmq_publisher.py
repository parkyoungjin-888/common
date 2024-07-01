import json
import pika


class RabbitmqPublisher:
    def __init__(self, user: str, password: str, host: str, port: int,
                 exchange: str, queue_list: list[str]):
        self.url = f'amqp://{user}:{password}@{host}:{port}'
        self.exchange = exchange
        self.queue_list = queue_list

        with pika.BlockingConnection(pika.URLParameters(self.url)) as connection:
            with connection.channel() as channel:
                channel.exchange_declare(exchange=self.exchange, exchange_type='fanout')
                for queue in self.queue_list:
                    channel.queue_declare(queue=queue, durable=True)
                    channel.queue_bind(queue=queue, exchange=self.exchange)

    def publish(self, messages: list[dict], batch_size: int = 10) -> None:
        with pika.BlockingConnection(pika.URLParameters(self.url)) as connection:
            with connection.channel() as channel:
                channel.tx_select()
                try:
                    for i, message in enumerate(messages):
                        byte_message = json.dumps(message).encode('utf-8')
                        channel.basic_publish(exchange=self.exchange, routing_key='', body=byte_message)
                        if (i + 1) % batch_size == 0 or (i + 1) == len(messages):
                            channel.tx_commit()
                except Exception as e:
                    print(f'error in RabbitmqPublisher publish : {e}')
                    channel.tx_rollback()
