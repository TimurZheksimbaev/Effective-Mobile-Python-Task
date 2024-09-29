from fastapi import Depends
from repositories.product_repository import get_product_repository
from repositories.product_repository import ProductRepository

class ProductService:
    def __init__(self, product_repo: ProductRepository):
        self.product_repo = product_repo

    # Creating a new product
    async def create_product(self, product_data: dict):
        return await self.product_repo.create(product_data)

    # Fetching the list of all products
    async def list_products(self):
        return await self.product_repo.list()

    # Fetching a specific product by ID
    async def get_product(self, product_id: int):
        product = await self.product_repo.get(product_id)
        if not product:
            raise ValueError(f"Product with ID {product_id} not found")
        return product

    # Updating a product by ID
    async def update_product(self, product_id: int, product_data: dict):
        product = await self.get_product(product_id)
        return await self.product_repo.update(product_id, product_data)

    # Deleting a product by ID
    async def delete_product(self, product_id: int):
        product = await self.get_product(product_id)
        return await self.product_repo.delete(product_id)

def get_product_service(product_repo: ProductRepository = Depends(get_product_repository)):
    return ProductService(product_repo)
