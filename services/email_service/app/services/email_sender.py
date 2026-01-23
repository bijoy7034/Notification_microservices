from jinja2 import Environment, FileSystemLoader
from email.mime.text import MIMEText
import smtplib

env = Environment(loader=FileSystemLoader('app/templates'))

def send_email(event):
    template = env.get_template(f"{event['template']}.html")
    html_content = template.render(**event['data'])
    msg = MIMEText(html_content, "html")
    
    msg["Subject"] = event['subject']
    msg["From"] = "noreply@example.com"
    msg["To"] = event["to"]
    
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login("EMAIL", "PASSWORD")
        server.send_message(msg)
        
    print("Email Sent")
