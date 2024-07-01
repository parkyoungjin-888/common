from kafka_module.kafka_consumer import KafkaConsumerControl


class TestControl:
    def __init__(self):
        self.kafka_consumer = KafkaConsumerControl('192.168.0.104', 9092, 'raw_data')
        self.temp_queue = []

    def test_call_back_func(self, data: dict):
        self.temp_queue.append(data)
        print(self.temp_queue)

    def run(self):
        self.kafka_consumer.start_consumer(self.test_call_back_func)

    def close(self):
        self.kafka_consumer.close()


if __name__ == '__main__':
    test_control = TestControl()
    test_control.run()
    test_control.close()
