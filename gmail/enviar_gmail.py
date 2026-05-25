import os
import smtplib

from dotenv import load_dotenv
from email.mime.text import MIMEText

load_dotenv()

SMTP_HOST = os.getenv("SERVER_SMTP")
SMTP_PORT = int(os.getenv("PORT_SMTP"))
SMTP_USER = os.getenv("USER_SMTP")
SMTP_PASSWORD = os.getenv("PASSWORD_SMTP")


def create_email(subject: str,body: str, to_email: str) -> MIMEText:

    msg = MIMEText(body, "plain", "utf-8")

    msg["From"] = SMTP_USER
    msg["To"] = to_email
    msg["Subject"] = subject

    return msg


def send_email(subject: str, body: str, to_email: str):

  
    msg = create_email(subject, body, to_email)

    try:
        print("INICIANDO SMTP")

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:

            server.starttls()

            server.login(SMTP_USER, SMTP_PASSWORD)

            server.send_message(msg)
            print("INICIANDO SMTP foi enviado")
        return True

    except Exception as e:

        print(f"SMTP Error: {e}")

        return False