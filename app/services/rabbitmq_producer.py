import aio_pika
import json


async def send_request_to_project_a(endpoint: str, method: str = 'GET',
                                    data: dict = None):
    # Подключаемся к RabbitMQ серверу
    connection = await aio_pika.connect_robust("amqp://localhost/")

    async with connection:
        async with connection.channel() as channel:
            # Формируем сообщение, которое включает метод и данные (если есть)
            message_body = {
                'endpoint': endpoint,
                'method': method,
                'data': data
            }

            # Публикуем сообщение в очередь
            await channel.default_exchange.publish(
                aio_pika.Message(body=json.dumps(message_body).encode()),
                routing_key='request_queue'
            )
            print(
                f" [x] Sent {method} request to {endpoint} with data: {data}")
