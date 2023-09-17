from celery import Celery
import smtplib
from email.message import EmailMessage
from decouple import config

celery = Celery(
    'tasks',
    broker=f'amqp://{config("BROKER_DOCKER_URL")}'
)


def send_email(username: str, user_email: str):
    email = EmailMessage()
    email['Subject'] = f'Добро пожаловать, {username}!'
    email['From'] = config("SMTP_USER")
    email['To'] = user_email
    email.set_content(f"Hello, {username}!\nWelcome to the BookTracker")
    return email


@celery.task
def email_after_registration(username: str, user_email: str):
    email = send_email(username, user_email)
    with smtplib.SMTP_SSL(config("SMTP_HOST"), config("SMTP_PORT")) as server:
        server.login(config("SMTP_USER"), config("SMTP_PASSWORD"))
        server.send_message(email)
