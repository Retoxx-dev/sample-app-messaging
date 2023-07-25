import json
from azure.communication.email import EmailClient

import settings


def auth_type():
    if (settings.ENV == 'development'):
        email_client = EmailClient.from_connection_string(settings.EMAIL_CONNECTION_STRING)
        return email_client


async def triage_email(message):
    data = json.loads(message)
    message_type = data['type']
    if message_type == 'welcome':
        settings.logging.info(f" [x] Received {message_type} email request")
        await send_welcome_email(data)
    elif message_type == 'reset_password':
        settings.logging.info(f" [x] Received {message_type} email request")
        await send_password_reset_email(data)
    else:
        settings.logging.info(f" [x] Received unknown email request type {message_type}")


async def send_welcome_email(data):
    settings.logging.info(f" [x] Sending welcome email to {data['email_address']}")
    message = {
        "content": {
            "subject": "Welcome to our service",
            "plainText": f"Welcome to our service {data['first_name']} {data['last_name']}",
            "html": f"<html><h1>Welcome to our service {data['first_name']} {data['last_name']}</h1></html>"
        },
        "recipients": {
            "to": [
                {
                    "address": f"{data['email_address']}"
                }
            ]
        },
        "senderAddress": f"{settings.SENDER_EMAIL}"
    }
    auth_type().begin_send(message)
    settings.logging.info(f" [x] Welcome email sent to {data['email_address']}")


async def send_password_reset_email(data):
    settings.logging.info(f" [x] Sending password reset email to {data['email_address']}")
    message = {
        "content": {
            "subject": "Password reset",
            "plainText": f"Hi {data['first_name']} {data['last_name']},\n\nYou have requested a password reset. Please use the following link to reset your password:\n\nhttp://localhost:3000/reset-password?token={data['token']}",
            "html": f"<html><h1>Hi {data['first_name']} {data['last_name']},</h1><br><p>You have requested a password reset. Please use the following link to reset your password:</p><br><a href='http://localhost:3000/reset-password?token={data['token']}'>https://localhost:3000/reset-password?token={data['token']}</a></html>"
        },
        "recipients": {
            "to": [
                {
                    "address": f"{data['email_address']}"
                }
            ]
        },
        "senderAddress": f"{settings.SENDER_EMAIL}"
    }
    auth_type().begin_send(message)
    settings.logging.info(f" [x] Password reset email sent to {data['email_address']}")
