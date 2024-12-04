import aio_pika


async def on_message(message: aio_pika.IncomingMessage):
    async with message.process():
        print(f"Received message: {message.body.decode()}")
        # Here, you can add logic to process the message, like updating MongoDB,
        # or doing something based on the received data.
