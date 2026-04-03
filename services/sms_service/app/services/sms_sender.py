import logging

logger = logging.getLogger(__name__)

def send_sms(event: dict):
    """
    Mock function to simulate sending an SMS notification.
    """
    logger.info(f"[SMS SENDER] Preparing to send SMS to {event.get('to')}")
    # In a real scenario, you would integrate Twilio, Vonage, etc. here
    # Example: twilio_client.messages.create(body=event['data'], to=event['to'], from_='+1234567890')
    
    logger.info(f"[SMS SENDER] SMS sent to {event.get('to')} with content: {event.get('data')}")
