import asyncio

from uvicorn import Config, Server

from app.rabbitmq_consumer import start_response_listener
from app.routers.product import product_router
from fastapi import FastAPI

routers = [product_router]

app = FastAPI()

for router in routers:
    app.include_router(router)


async def main():
    config = Config(app="main:app", host="0.0.0.0", port=8001, reload=True)
    server = Server(config)

    await asyncio.gather(
        server.serve()
    )


if __name__ == "__main__":
    asyncio.run(main())
