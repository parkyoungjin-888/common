import time
import json
import pika
from typing import Callable


class RabbitmqConsumer:
    def __init__(self, user: str, password: str, host: str, port: int,
                 exchange: str, queue: str, callback: Callable[[list[dict]], None],
                 max_message_size: int = 1000, max_interval_sec: int = 1):
        self.url = f'amqp://{user}:{password}@{host}:{port}'
        self.exchange = exchange
        self.queue = queue
        self.callback = callback
        self.max_message_size = max_message_size
        self.max_interval_sec = max_interval_sec if max_interval_sec < 600 else 600

        self.message_buffer = []
        self.delivery_tag_buffer = []
        self.last_callback_time = None

        with pika.BlockingConnection(pika.URLParameters(self.url)) as connection:
            with connection.channel() as channel:
                channel.exchange_declare(exchange=self.exchange, exchange_type='fanout')
                channel.queue_declare(queue=queue, durable=True)
                channel.queue_bind(queue=queue, exchange=self.exchange)

    def consuming(self) -> None:
        with pika.BlockingConnection(pika.URLParameters(self.url)) as connection:
            with connection.channel() as channel:
                channel.basic_qos(prefetch_count=0)

                while True:
                    after_time = time.time() - self.last_callback_time if self.last_callback_time is not None else 600
                    if len(self.message_buffer) > self.max_message_size or (
                            len(self.message_buffer) and after_time >= self.max_interval_sec):
                        try:
                            self.callback(self.message_buffer)
                            for delivery_tag in self.delivery_tag_buffer:
                                channel.basic_ack(delivery_tag)
                        except Exception as e:
                            print(f'error in RabbitmqConsumer callback : {e}')
                            for delivery_tag in self.delivery_tag_buffer:
                                channel.basic_nack(delivery_tag)
                        finally:
                            self.last_callback_time = time.time()
                            self.message_buffer = []
                            self.delivery_tag_buffer = []
                    else:
                        method, properties, body = channel.basic_get(queue=self.queue)
                        if body is not None:
                            decode_body = json.loads(body.decode('utf-8'))
                            self.message_buffer.append(decode_body)
                            self.delivery_tag_buffer.append(method.delivery_tag)
