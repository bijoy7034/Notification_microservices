import os
import smtplib
from jinja2 import Environment, FileSystemLoader
from email.mime.text import MIMEText
from app.core.config import settings
from app.core.logging import logger

env = Environment(loader=FileSystemLoader("app/templates"))

def send_email(event):
    logger.info(f"Preparing to send email to {event['to']} using template {event['template']}")
    if not settings.SMTP_USER or not settings.SMTP_PASS:
        logger.error("SMTP credentials are not set in environment variables")
        raise RuntimeError("SMTP credentials are not set in environment variables")

    template = env.get_template(f"{event['template']}.html")
    html_content = template.render(**event["data"])

    msg = MIMEText(html_content, "html")
    msg["Subject"] = event.get("subject", "Notification")
    msg["From"] = settings.SMTP_USER
    msg["To"] = event["to"]
    
    logger.info(f"Connecting to SMTP server {settings.SMTP_HOST}:{settings.SMTP_PORT}")

    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        logger.info("Starting TLS session")
        server.starttls()
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(msg)

    logger.info(f"Email successfully sent to {event['to']}")
