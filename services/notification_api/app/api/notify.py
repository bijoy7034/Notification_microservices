from fastapi import APIRouter
from app.schema.notification import NotificationRequest
from app.producers.rabitmq_producers import publish_notification

router = APIRouter(
    prefix="/notify",
    tags=["Notification API"],
)

@router.post("/")
async def send_notification(data: NotificationRequest):
    if data.channel == "email":
        message = {
            "to": data.to,
            "subject": data.subject,
            "template": data.template,
            "data": data.data
        }
        publish_notification(message, routing_key="email.queue")
        return {"message": "Email notification sent to the queue", "channel": data.channel}
    return {"message": "Notification sent"}