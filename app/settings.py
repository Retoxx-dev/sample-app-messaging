from os import environ
import logging

MANDATORY_ENV_VARS = ['RABBITMQ_CONNECTION_STRING',
                      'RABBITMQ_QUEUE_NAME',
                      'SENDER_EMAIL',
                      'EMAIL_CONNECTION_STRING'
                      ]


def check_env_vars():
    for var in MANDATORY_ENV_VARS:
        if var not in environ:
            raise ValueError(f'{var} environment variable is not set')


ENV = environ.get('ENV', 'development')
EMAIL_CONNECTION_STRING = environ.get('EMAIL_CONNECTION_STRING')
SENDER_EMAIL = environ.get('SENDER_EMAIL')

RABBITMQ_CONNECTION_STRING = environ.get('RABBITMQ_CONNECTION_STRING')
RABBITMQ_QUEUE_NAME = environ.get('RABBITMQ_QUEUE_NAME')


def require_connstring_dev():
    if (ENV == 'development' and EMAIL_CONNECTION_STRING not in environ):
        raise ValueError('EMAIL_CONNECTION_STRING is not set')


INFO_LOGGING_FORMAT = 'INFO:     %(asctime)s %(message)s'
WARNING_LOGGING_FORMAT = 'WARNING:     %(asctime)s %(message)s'


def configure_logging():
    ENV = environ.get('ENV', 'development')
    if ENV == 'production':
        logging.basicConfig(level=logging.INFO, format=WARNING_LOGGING_FORMAT)
        logging.info('Running in production mode')
    if ENV == 'development':
        logging.basicConfig(level=logging.INFO, format=INFO_LOGGING_FORMAT)
        logging.info('Running in development mode')
