from kafka import KafkaProducer
from json import dumps
from kafka_module.model.data_model import Rawdata, Imgdata


class KafkaProducerControl:
    def __init__(self, server_urls: list[str], topic: str):
        self.topic = topic
        self.producer = KafkaProducer(
            acks=0,
            compression_type='gzip',
            bootstrap_servers=server_urls,
            key_serializer=lambda k: k.encode('utf-8'),
            value_serializer=lambda x: dumps(x).encode('utf-8')
        )

    def send_data(self, data: Rawdata, key: str = None):
        try:
            if key is None:
                future = self.producer.send(self.topic, value=data.model_dump())
            else:
                future = self.producer.send(self.topic, value=data.model_dump(), key=key)
            result = future.get(timeout=10)  # 메시지 전송 결과를 기다림 (동기식)
            print(f"Message sent successfully: {result}")
        except Exception as e:
            print(f"Failed to send message: {e}")

    def send_img(self, img_data: Imgdata, key: str = None):
        try:
            if key is None:
                future = self.producer.send(self.topic, value=img_data.model_dump())
            else:
                future = self.producer.send(self.topic, value=img_data.model_dump(), key=key)
            result = future.get(timeout=10)
            print(f"Message sent successfully: {result}")
        except Exception as e:
            print(f"Failed to send message: {e}")

    def close(self):
        self.producer.flush()
        self.producer.close()

    def __del__(self):
        self.close()


if __name__ == '__main__':
    import cv2
    from datetime import datetime

    _server_urls = ['192.168.0.104:9091', '192.168.0.104:9092', '192.168.0.104:9093']

    kafka_producer = KafkaProducerControl(_server_urls, 'test_topic')

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    cap.set(cv2.CAP_PROP_FPS, 60)

    _key = 'test'

    while True:
        ret, img = cap.read()
        _timestamp = datetime.now().timestamp()

        # cv2.imshow('img', img)
        # cv2.waitKey(0)

        _img_data = Imgdata(name='test_img.jpg', timestamp=_timestamp,
                            width=img.shape[1], height=img.shape[0], img=img)
        kafka_producer.send_img(_img_data, key=_key)

        # _data = Rawdata(timestamp=1725188400, io_id='aaa', value=1.1)
        # kafka_producer.send_data(_data)

    print('end')
