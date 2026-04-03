import json
import pika
import logging
import os
import time
from app.services.push_sender import send_push

logger = logging.getLogger(__name__)

def callback(ch, method, properties, body):
    logger.info("Received Push Notification event from queue")
    try:
        event = json.loads(body)
        send_push(event)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        logger.error(f"Failed to process Push Notification event: {e}")

def start_consumer():
    rabbitmq_host = os.getenv("RABBITMQ_HOST", "rabbitmq")
    time.sleep(10) # wait for rabbitmq to initialize
    
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=rabbitmq_host)
    )
    logger.info(f"Connected to RabbitMQ at {rabbitmq_host}")
    channel = connection.channel()
    channel.queue_declare(queue="push.queue", durable=True)

    channel.basic_consume(
        queue="push.queue",
        on_message_callback=callback
    )

    print("Push Notification service started listening on push.queue...")
    channel.start_consuming()
