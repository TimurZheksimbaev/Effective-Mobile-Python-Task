from fastapi import Depends
from repositories.product_repository import get_product_repository
from repositories.product_repository import ProductRepository
from schemes.product_scheme import ProductCreate, ProductUpdate
from database.models import Product
from exceptions import NotFoundException, NotFoundItemsException

class ProductService:
    def __init__(self, product_repo: ProductRepository):
        self.product_repo = product_repo

    async def create_product(self, product_data: ProductCreate):
        data = Product(**product_data.dict())
        return await self.product_repo.create(data)

    async def list_products(self):
        products = await self.product_repo.list()
        if not products:
            raise NotFoundItemsException("products")
        return products

    async def get_product(self, product_id: int):
        product = await self.product_repo.get(product_id)
        if not product:
            # raise ValueError(f"Product with ID {product_id} not found")
            raise NotFoundException("product", product_id)
        return product

    async def update_product(self, product_id: int, product_data: ProductUpdate):
        data = product_data.dict(exclude_unset=True)
        product = await self.product_repo.update(product_id, data)
        if not product:
            raise NotFoundException("product", product_id)
        return product

    async def delete_product(self, product_id: int):
        product = await self.product_repo.delete(product_id)
        if not product:
            raise NotFoundException("product", product_id)
        return product


def get_product_service(product_repo: ProductRepository = Depends(get_product_repository)):
    return ProductService(product_repo)
