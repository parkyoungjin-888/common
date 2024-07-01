from kafka import KafkaProducer
from json import dumps
from kafka_module.model.raw_data_model import Rawdata


class KafkaProducerControl:
    def __init__(self, host: str, port: int, topic: str):
        self.topic = topic
        self.producer = KafkaProducer(acks=0,
                                      compression_type='gzip',
                                      bootstrap_servers=[f'{host}:{port}'],
                                      value_serializer=lambda x: dumps(x).encode('utf-8'))

    def send_data(self, data: Rawdata):
        self.producer.send(self.topic, value=data.model_dump())
