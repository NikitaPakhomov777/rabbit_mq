from fastapi import FastAPI, Request
from starlette.responses import JSONResponse
import pika
import json
import httpx
import threading

app = FastAPI()


def on_message_callback(ch, method, properties, body):
    # Получение сообщения из RabbitMQ
    message = json.loads(body)
    endpoints = message

    # Удаляем старые маршруты (если нужно)
    # Например, можно поддерживать список и обновлять его

    # Обработка каждого эндпоинта
    for endpoint in endpoints:
        path = endpoint['path']
        method = endpoint['method'].upper()

        async def dynamic_route(request: Request):
            async with httpx.AsyncClient() as client:
                try:
                    print(request)
                    print(request)
                    if request.method in ['POST', 'PUT', 'PATCH']:
                        json_data = await request.json()
                    else:
                        json_data = None
                except json.JSONDecodeError:
                    json_data = None  # Обрабатываем случай недействительного или пустого JSON

                response = await client.request(
                    method=request.method,
                    url=f'http://localhost:8000{request.url.path}',
                    params=request.query_params,
                    json=json_data
                )
                return JSONResponse(content=response.json(), status_code=response.status_code)


def start_consuming():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='endpoints_queue')

    channel.basic_consume(queue='endpoints_queue',
                          on_message_callback=on_message_callback,
                          auto_ack=True)

    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


# Запуск потребителя сообщений в фоне
threading.Thread(target=start_consuming, daemon=True).start()


@app.get('/test')
def test_endpoint():
    return {"message": "This is a test endpoint"}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
