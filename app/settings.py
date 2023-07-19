from os import environ
import logging

ENV = environ.get('ENV', 'development')
EMAIL_CONNECTION_STRING = environ.get('EMAIL_CONNECTION_STRING')
SENDER_EMAIL = environ.get('SENDER_EMAIL')

RABBITMQ_CONNECTION_STRING = environ.get('RABBITMQ_CONNECTION_STRING')
RABBITMQ_QUEUE_NAME = environ.get('RABBITMQ_QUEUE_NAME')

def require_connstring_dev():
    if (ENV == 'development' and EMAIL_CONNECTION_STRING not in environ):
        raise ValueError('EMAIL_CONNECTION_STRING is not set')
    
    
# INFO_LOGGING_FORMAT = 'INFO:     %(asctime)s %(message)s'
# if (ENV == 'development'):
#     logging.basicConfig(level=logging.INFO, format=INFO_LOGGING_FORMAT)