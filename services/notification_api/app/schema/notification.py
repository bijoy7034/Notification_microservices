from pydantic import BaseModel

class NotificationRequest(BaseModel):
    channel : str
    to: str
    subject: str
    template: str
    data: dict