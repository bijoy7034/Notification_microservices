import json
import pika
import logging
import os
import time
from app.services.sms_sender import send_sms

logger = logging.getLogger(__name__)

def callback(ch, method, properties, body):
    logger.info("Received SMS event from queue")
    try:
        event = json.loads(body)
        send_sms(event)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        logger.error(f"Failed to process SMS event: {e}")
        # Optionally nack it to re-queue
        # ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

def start_consumer():
    rabbitmq_host = os.getenv("RABBITMQ_HOST", "rabbitmq")
    time.sleep(10) # wait for rabbitmq to initialize
    
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=rabbitmq_host)
    )
    logger.info(f"Connected to RabbitMQ at {rabbitmq_host}")
    channel = connection.channel()
    channel.queue_declare(queue="sms.queue", durable=True)

    channel.basic_consume(
        queue="sms.queue",
        on_message_callback=callback
    )

    print("SMS service started listening on sms.queue...")
    channel.start_consuming()
