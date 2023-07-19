from rabbit_receiver import RabbitMQReceiver
import asyncio

import settings

async def main():
    receiver = RabbitMQReceiver(settings.RABBITMQ_CONNECTION_STRING, settings.RABBITMQ_QUEUE_NAME)
    await receiver.connect()
    await receiver.receive_message()
    
if __name__ == "__main__":
    asyncio.run(main())