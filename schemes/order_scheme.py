from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum

class OrderStatus(str, Enum):
    in_progress = "in_progress"
    shipped = "shipped"
    delivered = "delivered"

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int

class OrderCreate(BaseModel):
    items: List[OrderItemCreate]

class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int

    class Config:
        orm_mode = True

class OrderResponse(BaseModel):
    id: int
    created_at: datetime
    status: OrderStatus
    items: List[OrderItemResponse]

    class Config:
        orm_mode = True
