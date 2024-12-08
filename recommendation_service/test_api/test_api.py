from fastapi import FastAPI
import pika
import json

app = FastAPI()

RABBITMQ_HOST = "rabbitmq"  # Adjust this based on your setup
QUEUENAME_JOBSEEKER = "jobseeker_update"
QUEUENAME_JOB = "job_update"


@app.post("/publish/jobseeker")
async def publish_message(payload: dict):
    """
    Publish a message to RabbitMQ for testing the listener.
    Payload: JSON data to be sent to the queue.
    """
    try:
        # Connect to RabbitMQ
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        channel = connection.channel()

        # Declare the queue (optional, ensures the queue exists)
        channel.queue_declare(queue=QUEUENAME_JOBSEEKER, durable=True)

        # Publish the message
        message = json.dumps(payload)
        channel.basic_publish(exchange='', routing_key=QUEUENAME_JOBSEEKER, body=message)

        connection.close()
        return {"status": "success", "message": f"Message sent to queue '{QUEUENAME_JOBSEEKER}'", "data": payload}

    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.post("/publish/job")
async def publish_message(payload: dict):
    """
    Publish a message to RabbitMQ for testing the listener.
    Payload: JSON data to be sent to the queue.
    """
    try:
        # Connect to RabbitMQ
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        channel = connection.channel()

        # Declare the queue (optional, ensures the queue exists)
        channel.queue_declare(queue=QUEUENAME_JOB, durable=True)

        # Publish the message
        message = json.dumps(payload)
        channel.basic_publish(exchange='', routing_key=QUEUENAME_JOB, body=message)

        connection.close()
        return {"status": "success", "message": f"Message sent to queue '{QUEUENAME_JOB}'", "data": payload}

    except Exception as e:
        return {"status": "error", "message": str(e)}



@app.get("/test")
def test():
    return {"hi blud"}