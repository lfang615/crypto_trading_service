from aiokafka import AIOKafkaProducer
import json
import app.core.config as config

class KafkaProducer:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(KafkaProducer, cls).__new__(cls)
            cls._instance.init_producer(*args, **kwargs)
        return cls._instance

    def init_producer(self, *args, **kwargs):
        self.producer = AIOKafkaProducer(
            bootstrap_servers=config.KAFKA_URI
        )

    async def start(self):
        await self.producer.start()

    async def stop(self):
        await self.producer.stop()

    async def send_order(self, topic:str, order_id:str, client_oid:str):
        value = json.dumps({"orderId": order_id, "clientOid": client_oid})
        await self.producer.send_and_wait(topic, value=value)
