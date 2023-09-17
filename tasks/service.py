from email.message import EmailMessage
from decouple import config


def send_email(username: str, user_email: str):
    email = EmailMessage()
    email['Subject'] = f'Welcome, {username}!'
    email['From'] = config("SMTP_USER")
    email['To'] = user_email
    email.set_content(f"Hello, {username}!\nWelcome to the BookTracker")
    return email