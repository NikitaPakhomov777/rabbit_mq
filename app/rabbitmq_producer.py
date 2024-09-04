import aio_pika
import json


async def send_request_to_project_a(endpoint: str):
    # Подключаемся к RabbitMQ серверу
    connection = await aio_pika.connect_robust("amqp://localhost/")

    async with connection:
        async with connection.channel() as channel:
            # Объявляем очереди
            await channel.default_exchange.publish(
                aio_pika.Message(body=json.dumps({'endpoint': endpoint}).encode()),
                routing_key='request_queue'
            )
            print(f" [x] Sent request to {endpoint}")
