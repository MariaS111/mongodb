from celery import Celery
import smtplib
from service import send_email
from decouple import config


celery = Celery(
    'tasks',
    broker=f'amqp://{config("BROKER_DOCKER_URL")}'
)


@celery.task
def email_after_registration(username: str, user_email: str):
    email = send_email(username, user_email)
    with smtplib.SMTP_SSL(config("SMTP_HOST"), config("SMTP_PORT")) as server:
        server.login(config("SMTP_USER"), config("SMTP_PASSWORD"))
        server.send_message(email)
