from fastapi import APIRouter, HTTPException

from app.services.rabbitmq_consumer import start_response_listener
from app.services.rabbitmq_producer import send_request_to_project_a
from app.schemas.product_schemas import ProductCreate, ProductUpdate

product_router = APIRouter(
    prefix='/products', tags=['product']
)


@product_router.get('/get/')
async def get_products():
    await send_request_to_project_a("/products/get/")
    get_products_all = await start_response_listener()
    return get_products_all


@product_router.post('/add/')
async def create_product(product: ProductCreate):
    try:
        # Отправляем запрос на создание продукта в RabbitMQ
        await send_request_to_project_a("/products/add/", method='POST', data=product.model_dump())
        # Получаем ответ от слушателя
        response = await start_response_listener()
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@product_router.delete('/delete_product/{product_id}')
async def delete_product(product_id: int):
    try:
        # Отправляем запрос на удаление продукта в RabbitMQ
        await send_request_to_project_a(f"/products/delete_product/{product_id}", method='DELETE')
        # Получаем ответ от слушателя
        response = await start_response_listener()
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@product_router.patch('/update_product/')
async def update_product(product: ProductUpdate):
    try:
        await send_request_to_project_a(f"/products/update_product/", method='PATCH', data=product.model_dump())
        response = await start_response_listener()
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))