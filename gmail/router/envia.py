from fastapi import APIRouter, HTTPException

from gmail.enviar_gmail import send_email
from gmail.router.tasks import send_email_task, app
from gmail.schemas.enviar import EmailSchema

from celery.result import AsyncResult


router = APIRouter(prefix="/v1/email", tags=["Email"])

@router.post("/v2/send")
def email_send_api_v2(payload: EmailSchema):

    ok = send_email(subject=payload.subject, body=payload.body, to_email=payload.to)
    
    if not ok:
        return HTTPException(status_code=500, detail="Failed to send email")
    
    return {
        "success": True,
        "message":"Email queued successfully",
    }

@router.post("/send")
def email_send_api(payload: EmailSchema):

    task = send_email_task.delay(subject=payload.subject, body=payload.body, to_email=payload.to)

    return {
        "success": True,
        "message":"Email queued successfully",
        "task_id":task.id
    }


@router.get("/status/{task_id}")
def task_status(task_id: str):

    task = AsyncResult(task_id, app=app)

    return {"task_id": task.id, "status": task.status,"result": task.result}