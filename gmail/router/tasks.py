from gmail.enviar_gmail import send_email 

from celery import Celery

app = Celery(

    "email_tasks",

    broker="redis://localhost:6379/0",

    backend="redis://localhost:6379/0"
)

@app.task
def send_email_task(subject, body, to_email):

    return send_email(subject=subject, body=body, to_email=to_email)