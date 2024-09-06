from fastapi import APIRouter

from app.services.rabbitmq_consumer import start_response_listener
from app.services.rabbitmq_producer import send_request_to_project_a


endpoint_calls_router = APIRouter(
    prefix='/endpoints', tags=['endpoints']
)

@endpoint_calls_router.get('/get/')
async def get_calls_count():
    await send_request_to_project_a("/endpoints/get_calls_count/")
    get_customers_all = await start_response_listener()
    return get_customers_all
