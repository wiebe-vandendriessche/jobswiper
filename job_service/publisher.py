# message publisher adapter
import asyncio
import json
import logging

from aio_pika import Message, connect_robust

from domain_model import Job
from interfaces import IChangedJobPublisher


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(message)s")


class ChangedJobPublisher(IChangedJobPublisher):
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

    async def job_created(self, job: Job):
        await self.__send_message(job)

    async def job_updated(self, job: Job):
        await self.__send_message(job)

    async def job_deleted(self, job: Job):
        await self.__send_message(job)

    async def __send_message(self, message: Job):
        # Convert payload to JSON and encode to bytes
        message_body = json.dumps(message.to_dict()).encode()
        # Publish the message to the queue
        await self.channel.default_exchange.publish(
            Message(body=message_body),
            routing_key=self.queue_name,  # Target the appropriate queue
        )
        logger.info(f"Message published on bus '{self.queue_name}'")
