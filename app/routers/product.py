from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from rabbitmq_consumer import start_response_listener
from rabbitmq_producer import send_request_to_project_a

product_router = APIRouter(
    prefix='/products', tags=['product']
)


@product_router.get('/get/')
async def get_products():
    await send_request_to_project_a("/products/get/")
    get_products_all = await start_response_listener()
    return get_products_all


# @product_router.post('/add/')
# async def create_product(product: ProductCreate, session: AsyncSession = Depends(get_async_session)):
#     new_product = await ProductCrud.post_new_product(product, session)
#     return new_product
#
#
# @product_router.delete('/delete_product/{product_id}')
# async def delete_product(product_id: int, session: AsyncSession = Depends(get_async_session)):
#     deleted_product = await ProductCrud.delete_product(product_id, session)
#     return deleted_product
#
#
# @product_router.patch('/update_product/')
# async def update_product(product: ProductUpdate, session: AsyncSession = Depends(get_async_session)):
#     updated_product = await ProductCrud.update_product(product, session)
#     return updated_product
