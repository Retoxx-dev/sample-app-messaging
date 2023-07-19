import aio_pika
import email_sender
import settings

class RabbitMQReceiver:
    def __init__(self, connection_string, queue_name):
        self.connection_string = connection_string
        self.queue_name = queue_name
        self.connection = None
        self.channel = None
        self.queue = None

    async def connect(self):
        # Create a connection to RabbitMQ
        self.connection = await aio_pika.connect_robust(
            self.connection_string,
            heartbeat=60,  # Set the heartbeat interval in seconds
            on_connection_lost=self.on_connection_lost
        )

        # Create a channel
        self.channel = await self.connection.channel()

        # Declare the queue to consume messages from
        self.queue = await self.channel.declare_queue(self.queue_name, durable=True)

    async def receive_message(self):
        if not self.connection:
            raise RuntimeError("RabbitMQ connection is not initialized.")

        async with self.queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    # Process the received message
                    message_body = message.body.decode()
                    print(f"Received message: {message_body}")
                    await email_sender.triage_email(message_body)

    async def close(self):
        if self.connection:
            await self.connection.close()
    
    def on_connection_lost(self, connection, exception):
        settings.logging.warning(f"Connection to RabbitMQ lost: {exception}")
