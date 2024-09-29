from pydantic import BaseModel
from typing import List
from datetime import datetime
from enum import Enum

# Модель для зранения статусов заказа
class OrderStatus(str, Enum):
    in_progress = "в процессе"
    shipped = "отправлен"
    delivered = "доставлен"

# Модель для создания единцы товара
class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int

# Модель для создания заказа
class OrderCreate(BaseModel):
    items: List[OrderItemCreate]

# Модель для ответа с информацией о единице товара
class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int

    class Config:
        orm_mode = True

# Модель для ответа с информацией о заказе
class OrderResponse(BaseModel):
    id: int
    created_at: datetime
    status: OrderStatus
    items: List[OrderItemResponse]

    class Config:
        orm_mode = True
