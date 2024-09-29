from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Order
from database.connect import get_db
from fastapi import Depends

class OrderRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, order: Order):
        self.db.add(order)
        await self.db.commit()
        await self.db.refresh(order)
        return order

    async def get(self, order_id: int):
        result = await self.db.execute(select(Order).where(Order.id == order_id))
        return result.scalar_one_or_none()

    async def list(self):
        result = await self.db.execute(select(Order))
        return result.scalars().all()

    async def update_status(self, order_id: int, status):
        order = await self.get(order_id)
        if order:
            order.status = status
            await self.db.commit()
        return order

def get_order_repository(db: AsyncSession = Depends(get_db)):
    return OrderRepository(db)
