from fastapi import APIRouter, HTTPException

from app.services.rabbitmq_consumer import start_response_listener
from app.services.rabbitmq_producer import send_request_to_project_a
from app.schemas.customer_schemas import CustomerCreate, CustomerUpdate

customer_router = APIRouter(
    prefix='/customers', tags=['customer']
)


@customer_router.get('/get/')
async def get_customers():
    await send_request_to_project_a("/customers/get/")
    get_customers_all = await start_response_listener()
    return get_customers_all


@customer_router.post('/add/')
async def create_customer(customer: CustomerCreate):
    try:
        # Отправляем запрос на создание продукта в RabbitMQ
        await send_request_to_project_a("/customers/add/", method='POST', data=customer.model_dump())
        # Получаем ответ от слушателя
        response = await start_response_listener()
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@customer_router.delete('/delete_customer/{customer_id}')
async def delete_customer(id_customer: int):
    try:
        # Отправляем запрос на удаление продукта в RabbitMQ
        await send_request_to_project_a(f"/customers/delete_customer/{id_customer}/", method='DELETE')
        # Получаем ответ от слушателя
        response = await start_response_listener()
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@customer_router.patch('/update_customer/')
async def update_customer(customer: CustomerUpdate):
    try:
        await send_request_to_project_a(f"/customers/update_customer/", method='PATCH', data=customer.model_dump())
        response = await start_response_listener()
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
