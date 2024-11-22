import ssl

from fastapi import FastAPI, HTTPException, BackgroundTasks, Header
from pydantic import BaseModel, EmailStr
from email.message import EmailMessage
import smtplib
import logging

# Initialize the FastAPI app
app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration for the Gmail SMTP server
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465


def send_email_background(subject: str, body: str, recipient_email: str, smtp_username: str, smtp_password: str):
    try:
        msg = EmailMessage()
        msg.set_content(body)
        msg["Subject"] = subject
        msg["From"] = smtp_username
        msg["To"] = recipient_email

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
            server.set_debuglevel(1)
            logger.info("Connected to SMTP server")
            server.login(smtp_username, smtp_password)
            logger.info("Logged into SMTP server")
            server.send_message(msg)
            logger.info("Email sent successfully")
        logger.info(f"Email sent successfully to {recipient_email}")
    except smtplib.SMTPConnectError:
        logger.error("Failed to connect to the SMTP server. Service not available.")
    except smtplib.SMTPAuthenticationError:
        logger.error("Invalid SMTP username or password. Authentication failed.")
    except smtplib.SMTPRecipientsRefused:
        logger.error(f"Recipient email address {recipient_email} is invalid.")
    except Exception as e:
        logger.error(f"An unexpected error occurred while sending the email: {e}")


class EmailRequest(BaseModel):
    subject: str
    body: str
    recipient_email: EmailStr


@app.get("/")
async def root():
    return {"message": "Mail Delivery Service is running"}


@app.post("/send-email/")
async def send_email(
        email_request: EmailRequest,
        background_tasks: BackgroundTasks,
        smtp_username: str = Header(...),
        smtp_password: str = Header(...),
):
    try:
        background_tasks.add_task(
            send_email_background,
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
