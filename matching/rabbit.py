import asyncio
import time
import json
import logging
import uuid
from aio_pika import Message, connect_robust

from domain_model import Recommendation
from interfaces import IMatchPublisher

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(message)s")


class PikaConsumer:

    def __init__(self, host, port, queue_name, consumer_function):
        self.host = host
        self.process_callable = consumer_function
        self.queue_name = queue_name
        self.port = port
        self.connection = None
        self.channel = None
        self.callback_queue = None
        self.response = None

    async def consume(self, loop):

        retry_attempts = 0
        while True:
            try:
                self.connection = await connect_robust(
                    host=self.host, port=self.port, loop=loop, heartbeat=0
                )
                self.channel = await self.connection.channel()
                queue = await self.channel.declare_queue(self.queue_name, durable=True)
                await queue.consume(self.process_callable, no_ack=False)
                logger.info("Pika connection initialized")
                return self.connection
            except Exception as e:
                retry_attempts += 1
                logger.warning(
                    f"Failed to connect to RabbitMQ (attempt {retry_attempts}). Retrying in 5 seconds... Error: {e}"
                )
                await asyncio.sleep(5)


class PikaPublisher(IMatchPublisher):
    def __init__(self, host, port, queue_name) -> None:
        self.host = host
        self.port = port
        self.queue_name = queue_name
        self.channel = None
        self.queue = None

    async def initialize(self):
        retry_attempts = 0
        while True:
            try:
                connection = await connect_robust(host=self.host, port=self.port)
                self.channel = await connection.channel()
                self.queue = await self.channel.declare_queue(
                    self.queue_name, durable=True
                )
                logger.info("Established pika async connection")
                break  # Connection successful, exit loop
            except Exception as e:
                retry_attempts += 1
                logger.warning(
                    f"Failed to connect to RabbitMQ for consuming (attempt {retry_attempts}). Retrying in 5 seconds... Error: {e}"
                )
                await asyncio.sleep(5)  # Async sleep for retrying

    async def found_match(self, message: Recommendation):
        # Convert payload to JSON and encode to bytes
        message_body = message.to_json().encode()
        # Publish the message to the queue
        await self.channel.default_exchange.publish(
            Message(body=message_body),
            routing_key=self.queue_name,  # Target the appropriate queue
        )
        logger.info(f"Message published on bus '{self.queue_name}'")
