# main.py

from fastapi import FastAPI, HTTPException, BackgroundTasks, Header
from pydantic import BaseModel, EmailStr
import logging

# Import the send_email function from email_utils
from email_utils import send_email

app = FastAPI()

logger = logging.getLogger(__name__)


class EmailRequest(BaseModel):
    subject: str
    body: str
    recipient_email: EmailStr


@app.get("/")
async def root():
    return {"message": "Mail Delivery Service is running"}


@app.post("/send-email/")
async def send_email_endpoint(
        email_request: EmailRequest,
        background_tasks: BackgroundTasks,
        smtp_username: str = Header(...),
        smtp_password: str = Header(...),
):
    try:
        background_tasks.add_task(
            send_email,
            email_request.subject,
            email_request.body,
            email_request.recipient_email,
            smtp_username,
            smtp_password,
        )
        return {"message": "Email is being sent in the background."}
    except Exception as e:
        logger.error(f"Failed to schedule email task: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred while processing the request.")
