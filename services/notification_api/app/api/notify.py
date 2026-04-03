from fastapi import APIRouter
from app.schema.notification import NotificationRequest
from app.producers.rabitmq_producers import publish_notification

router = APIRouter(
    prefix="/notify",
    tags=["Notification API"],
)

@router.post("/")
async def send_notification(data: NotificationRequest):
    message = {
        "to": data.to,
        "subject": data.subject,
        "template": data.template,
        "data": data.data
    }
    
    if data.channel == "email":
        publish_notification(message, routing_key="email.queue")
        return {"message": "Email notification sent to the queue", "channel": data.channel}
    elif data.channel == "sms":
        publish_notification(message, routing_key="sms.queue")
        return {"message": "SMS notification sent to the queue", "channel": data.channel}
    elif data.channel == "push":
        publish_notification(message, routing_key="push.queue")
        return {"message": "Push notification sent to the queue", "channel": data.channel}
        
    return {"error": "Unsupported channel", "channel": data.channel}