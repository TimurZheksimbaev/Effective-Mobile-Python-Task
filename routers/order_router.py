from fastapi import APIRouter, Depends, HTTPException
from services.order_service import get_order_service, OrderService
from schemes.order_scheme import OrderCreate, OrderResponse
from typing import List
from exceptions import NotEnoughStockException, NotFoundException, NotFoundItemsException, InvalidStatusException
from fastapi.encoders import jsonable_encoder

# Create the router for orders
order_router = APIRouter(
    prefix="/orders",
)

@order_router.post("/", responses={
    200: {"model": OrderResponse},
    400: {"description": "Not enough stock"}
})
async def create_order(
    order_data: OrderCreate,
    order_service: OrderService = Depends(get_order_service)
):
    try:
        return await order_service.create_order(order_data)
    except NotEnoughStockException as e:
        raise HTTPException(status_code=400, detail=str(e))

@order_router.get("/", responses={
    200: {"model": List[OrderResponse]},
    404: {"description": "No orders found"}
})
async def list_orders(order_service: OrderService = Depends(get_order_service)):
    try:
        return await order_service.list_orders()
    except NotFoundItemsException as e:
        return HTTPException(status_code=404, detail=str(e))

@order_router.get("/{id}", responses={
    200: {"model": OrderResponse},
    404: {"description": "Order not found"}
})
async def get_order(
    id: int,
    order_service: OrderService = Depends(get_order_service)
):
    try:
        return await order_service.get_order(id)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@order_router.put("/{order_id}", responses={
    200: {"model": OrderResponse},
    404: {"description": "Order not found"},
    400: {"description": "Invalid status"}
})
async def update_order_status(
    order_id: int,
    status: str,
    order_service: OrderService = Depends(get_order_service)
):
    try:
        return await order_service.update_order_status(order_id, status)
    except InvalidStatusException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
