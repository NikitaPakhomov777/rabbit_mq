from fastapi import APIRouter, HTTPException

from app.services.rabbitmq_consumer import start_response_listener
from app.services.rabbitmq_producer import send_request_to_project_a
from app.schemas.sale_schemas import SaleCreate, SaleUpdate

sale_router = APIRouter(
    prefix='/sales', tags=['sale']
)


@sale_router.get('/get/')
async def get_sales():
    await send_request_to_project_a("/sales/get/")
    get_sales_all = await start_response_listener()
    return get_sales_all


@sale_router.post('/add/')
async def create_customer(sale: SaleCreate):
    try:
        await send_request_to_project_a("/sales/add/", method='POST', data=sale.model_dump())
        response = await start_response_listener()
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@sale_router.delete('/delete_sale/{sale_id}')
async def delete_sale(sale_id: int):
    try:
        # Отправляем запрос на удаление продукта в RabbitMQ
        await send_request_to_project_a(f"/sales/delete_sale/{sale_id}", method='DELETE')
        # Получаем ответ от слушателя
        response = await start_response_listener()
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@sale_router.patch('/update_customer/')
async def update_sale(sale: SaleUpdate):
    try:
        await send_request_to_project_a(f"/sales/update_sale/", method='PATCH', data=sale.model_dump())
        response = await start_response_listener()
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
