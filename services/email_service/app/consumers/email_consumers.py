import json
import pika
from app.services.email_sender import send_email
from app.core.logging import logger

def callback(ch, method, properties, body):
    logger.info("Received email event from queue")
    event = json.loads(body)
    send_email(event)
    ch.basic_ack(delivery_tag=method.delivery_tag)

def start_consumer():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters("rabbitmq")
    )
    logger.info("Connected to RabbitMQ")
    channel = connection.channel()
    channel.queue_declare(queue="email.queue", durable=True)

    channel.basic_consume(
        queue="email.queue",
        on_message_callback=callback
    )

    print("Email service started...")
    channel.start_consuming()
