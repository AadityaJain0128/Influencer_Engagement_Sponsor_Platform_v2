from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


SMTP_HOST = "localhost"
SMTP_PORT = 1025
SENDER_EMAIL = "iescp@gmail.com"
SENDER_PASSWORD = "supersecretpassword"


def send_email(to, subject, content):
    msg = MIMEMultipart()
    msg["To"] = to
    msg["From"] = SENDER_EMAIL
    msg["Subject"] = subject
    msg.attach(MIMEText(content, "html"))
    client = SMTP(host=SMTP_HOST, port=SMTP_PORT)
    client.send_message(msg)
    client.quit()


# send_email(to="demo@gmail.com", subject="Test", content="<h1>Test Email</h1>")