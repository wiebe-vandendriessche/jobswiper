import asyncio
import time
import json
import logging
import uuid
from aio_pika import connect_robust

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
