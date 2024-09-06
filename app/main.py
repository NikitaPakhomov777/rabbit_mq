import uvicorn
from app.routers.product import product_router
from app.routers.customer import customer_router
from app.routers.sale import sale_router
from app.routers.endpoint_call_count import endpoint_calls_router
from fastapi import FastAPI

routers = [product_router, customer_router, sale_router, endpoint_calls_router]

app = FastAPI()

for router in routers:
    app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
