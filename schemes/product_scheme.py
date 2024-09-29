from pydantic import BaseModel
from typing import Optional

# Модель для создания товара
class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: int

# Модель для обноваления товара
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None

# Модель для ответа с информацией о товаре
class ProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    stock: int

    class Config:
        orm_mode = True
