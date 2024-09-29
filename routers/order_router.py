from fastapi import APIRouter
from services.order_service import get_order_service

order_router = APIRouter(
    prefix="/products"
)


@order_router.post("/")
async def create_order():
