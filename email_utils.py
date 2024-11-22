import ssl
import smtplib
from email.message import EmailMessage
import logging

logger = logging.getLogger(__name__)

# Configuration for the SMTP server (can be parameterized)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465  # For SSL


def send_email(subject: str, body: str, recipient_email: str, smtp_username: str, smtp_password: str):
    try:
        # Create the email message
        msg = EmailMessage()
        msg.set_content(body)
        msg["Subject"] = subject
        msg["From"] = smtp_username
        msg["To"] = recipient_email

        # Create a secure SSL context
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
            server.set_debuglevel(0)
            logger.info("Connecting to SMTP server")
            server.login(smtp_username, smtp_password)
            logger.info("Logged into SMTP server")
            server.send_message(msg)
            logger.info(f"Email sent successfully to {recipient_email}")
    except smtplib.SMTPConnectError:
        logger.error("Failed to connect to the SMTP server. Service not available.")
        raise
    except smtplib.SMTPAuthenticationError:
        logger.error("Invalid SMTP username or password. Authentication failed.")
        raise
    except smtplib.SMTPRecipientsRefused:
        logger.error(f"Recipient email address {recipient_email} is invalid.")
        raise
    except smtplib.SMTPException as e:
        logger.error(f"SMTP error occurred: {e}")
        raise
    except Exception as e:
        logger.error(f"An unexpected error occurred while sending the email: {e}")
        raise
