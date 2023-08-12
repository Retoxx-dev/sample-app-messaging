from fastapi import FastAPI
from rabbit_receiver import RabbitMQReceiver

import asyncio
import settings

app = FastAPI()


async def background_task(receiver: RabbitMQReceiver):
    await receiver.receive_message()


@app.on_event("startup")
async def startup_event():
    settings.configure_logging()
    settings.check_env_vars()
    receiver = RabbitMQReceiver(settings.RABBITMQ_CONNECTION_STRING, settings.RABBITMQ_QUEUE_NAME)
    await receiver.connect()
    app.state.receiver = receiver
    asyncio.create_task(background_task(receiver))


@app.get("/health", tags=["healthcheck"])
async def healthcheck_route():
    return {"status": "ok"}
