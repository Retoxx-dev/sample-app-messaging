import json
from azure.communication.email import EmailClient
from jinja2 import Environment, FileSystemLoader, select_autoescape
import settings

template_dir = './email_templates'
env = Environment(
    loader=FileSystemLoader(template_dir),
    autoescape=select_autoescape(['html', 'xml'])
)


def auth_type():
    # if (settings.ENV == 'development'): Disabled until AKS managed Identity is configured with Azure Comm Services
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
    template = env.get_template('welcome.html')
    message = {
        "content": {
            "subject": "Welcome to our service",
            "plainText": f"Welcome to our service {data['first_name']} {data['last_name']}",
            "html": template.render(first_name=data['first_name'],
                                    last_name=data['last_name'],
                                    client_url=settings.CLIENT_URL)
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
    template = env.get_template('password_reset.html')
    password_reset_url = f"{settings.CLIENT_URL}/reset-password?token={data['token']}"
    message = {
        "content": {
            "subject": "Password reset",
            "plainText": f"Please use the following link to reset your password:\n\n{password_reset_url}",
            "html": template.render(first_name=data['first_name'],
                                    last_name=data['last_name'],
                                    reset_link=password_reset_url)
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
