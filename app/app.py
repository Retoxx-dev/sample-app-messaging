from fastapi import FastAPI
from rabbit_receiver import RabbitMQReceiver

import settings

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    settings.configure_logging()
    settings.check_env_vars()
    receiver = RabbitMQReceiver(settings.RABBITMQ_CONNECTION_STRING, settings.RABBITMQ_QUEUE_NAME)
    await receiver.connect()
    await receiver.receive_message()


@app.get("/health", status_code=200)
async def healthcheck():
    return {"status": "ok"}
