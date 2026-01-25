import pika
import json
import os

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", 5672))


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT)
)
channel = connection.channel()


channel.queue_declare(queue="email.queue", durable=True)


message = {
    "notification_id": "test-001",
    "type": "EMAIL",
    "subject": "Payment",
    "to": "blessy.anil777@gmail.com",  
    "template": "payment_success",
    "data": {
        "name": "Bijoy",
        "amount": "499"
    }
}

channel.basic_publish(
    exchange="",
    routing_key="email.queue",
    body=json.dumps(message),
    properties=pika.BasicProperties(
        delivery_mode=2 
    )
)

print("Test email event published")
connection.close()
