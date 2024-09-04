import aio_pika
import json


async def start_response_listener():
    # Подключаемся к RabbitMQ серверу
    connection = await aio_pika.connect_robust("amqp://localhost/")

    async with connection:
        async with connection.channel() as channel:
            # Объявляем очередь для прослушивания
            queue = await channel.declare_queue('response_queue')

            async for message in queue:
                async with message.process():
                    # Декодируем и обрабатываем JSON ответ
                    response_data = json.loads(message.body.decode())
                    print(" [x] Received response data")

                    # Пример обработки JSON-ответа
                    status_code = response_data.get('status_code', 'No status code')
                    content = response_data.get('content', {})

                    print(f"Status Code: {status_code}")
                    print("Content:")
                    print(content)  # Обработка содержимого JSON

                    return content
