import aio_pika
import json
import logging
from core.config import settings

logger = logging.getLogger(__name__)

class RabbitMQPublisher:
    def __init__(self, url: str):
        self.url = url
        self.connection = None
        self.channel = None
        self.exchange = None

    async def connect(self):
        try:
            self.connection = await aio_pika.connect_robust(self.url)
            self.channel = await self.connection.channel()
            # Define an exchange for product events
            self.exchange = await self.channel.declare_exchange(
                "product_events", aio_pika.ExchangeType.TOPIC, durable=True
            )
            logger.info("Connected to RabbitMQ and declared exchange 'product_events'")
        except Exception as e:
            logger.error(f"Failed to connect to RabbitMQ: {e}")

    async def close(self):
        if self.connection:
            await self.connection.close()
            logger.info("RabbitMQ connection closed")

    async def publish_event(self, routing_key: str, message: dict):
        if not self.exchange:
            logger.warning("RabbitMQ exchange not initialized. Event not sent.")
            return
        try:
            message_body = json.dumps(message).encode()
            await self.exchange.publish(
                aio_pika.Message(body=message_body, delivery_mode=aio_pika.DeliveryMode.PERSISTENT),
                routing_key=routing_key,
            )
            logger.info(f"Published event '{routing_key}'")
        except Exception as e:
            logger.error(f"Failed to publish event to RabbitMQ: {e}")

# Global instance
rabbitmq_publisher = RabbitMQPublisher(settings.rabbitmq_url)
