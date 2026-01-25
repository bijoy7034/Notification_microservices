import json
import pika
from app.core.config import RABBITMQ_HOST, RABBITMQ_PORT


def publish_notification(message: dict, routing_key: str):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT)
    )
    
    channel = connection.channel()
    
    channel.basic_publish(
        exchange="",
        routing_key=routing_key,
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=2 
        )
    )
    
    connection.close()