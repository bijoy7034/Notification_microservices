import os
import smtplib
from jinja2 import Environment, FileSystemLoader
from email.mime.text import MIMEText

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")

env = Environment(loader=FileSystemLoader("app/templates"))

def send_email(event):
    if not SMTP_USER or not SMTP_PASS:
        raise RuntimeError("SMTP credentials are not set in environment variables")

    template = env.get_template(f"{event['template']}.html")
    html_content = template.render(**event["data"])

    msg = MIMEText(html_content, "html")
    msg["Subject"] = event.get("subject", "Notification")
    msg["From"] = SMTP_USER
    msg["To"] = event["to"]

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)

    print(f"Email sent to {event['to']}")
