from fastapi import Depends
from repositories.product_repository import get_product_repository
from repositories.product_repository import ProductRepository
from schemes.product_scheme import ProductCreate, ProductUpdate

class ProductService:
    def __init__(self, product_repo: ProductRepository):
        self.product_repo = product_repo

    async def create_product(self, product_data: ProductCreate):
        return await self.product_repo.create(product_data.dict())

    async def list_products(self):
        return await self.product_repo.list()

    async def get_product(self, product_id: int):
        product = await self.product_repo.get(product_id)
        if not product:
            raise ValueError(f"Product with ID {product_id} not found")
        return product

    async def update_product(self, product_id: int, product_data: ProductUpdate):
        return await self.product_repo.update(product_id, product_data.dict(exclude_unset=True))

    async def delete_product(self, product_id: int):
        return await self.product_repo.delete(product_id)


def get_product_service(product_repo: ProductRepository = Depends(get_product_repository)):
    return ProductService(product_repo)
