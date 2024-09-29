from fastapi import APIRouter
from order_router import order_router
from  product_router import product_router


api_router = APIRouter(
    prefix="/api"
)

api_router.include_router(order_router)
api_router.include_router(product_router)