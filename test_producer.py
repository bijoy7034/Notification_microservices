import pika
import json
import os

# RabbitMQ config
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", 5672))

# Connect to RabbitMQ
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT)
)
channel = connection.channel()

# Ensure the queue exists
channel.queue_declare(queue="email.queue", durable=True)

# Test email event
message = {
    "notification_id": "test-001",
    "type": "EMAIL",
    "subject": "Payment",
    "to": "bijoyanil74@gmail.com",  # Replace with your email
    "template": "payment_success",
    "data": {
        "name": "Bijoy",
        "amount": "499"
    }
}

# Publish message
channel.basic_publish(
    exchange="",
    routing_key="email.queue",
    body=json.dumps(message),
    properties=pika.BasicProperties(
        delivery_mode=2  # Make message persistent
    )
)

print("Test email event published")
connection.close()
