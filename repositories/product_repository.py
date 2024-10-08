from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Product
from database.connect import get_db
from fastapi import Depends

"""Класс для взаимодействия с таблицей товаров"""
class ProductRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    # Создание
    async def create(self, product: Product):
        self.db.add(product)
        await self.db.commit()
        await self.db.refresh(product)
        return product

    # Получение по ID
    async def get(self, product_id: int):
        result = await self.db.execute(select(Product).where(Product.id == product_id))
        return result.scalars().first()

    # Получение списка
    async def list(self):
        result = await self.db.execute(select(Product))
        return result.scalars().all()

    # Обновление
    async def update(self, product_id: int, product_data: dict):
        product = await self.get(product_id)
        if product:
            for key, value in product_data.items():
                setattr(product, key, value)
            await self.db.commit()
        return product

    # Удаление
    async def delete(self, product_id: int):
        product = await self.get(product_id)
        if product:
            await self.db.delete(product)
            await self.db.commit()
        return product

def get_product_repository(db: AsyncSession = Depends(get_db)):
    return ProductRepository(db)
