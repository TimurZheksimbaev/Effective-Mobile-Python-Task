from typing import List

from fastapi import APIRouter, Depends, HTTPException
from services.product_service import get_product_service, ProductService
from schemes.product_scheme import ProductCreate, ProductUpdate, ProductResponse
from exceptions import NotFoundException, NotFoundItemsException

product_router = APIRouter(
    prefix="/products",
)

@product_router.post("/", responses={
    200: {"model": ProductResponse}
})
async def create_product(product: ProductCreate, product_service: ProductService = Depends(get_product_service)):
    new_product = await product_service.create_product(product)
    return new_product

@product_router.get("/", responses={
    200: {"model": List[ProductResponse]},
    404: {"description": "No products found"}
})
async def list_products(product_service: ProductService = Depends(get_product_service)):
    try:
        products = await product_service.list_products()
        return products
    except NotFoundItemsException as e:
        return HTTPException(status_code=404, detail=str(e))

@product_router.get("/{id}", responses={
    200: {"model": ProductResponse},
    404: {"description": "No products found"}
})
async def get_product_by_id(id: int, product_service: ProductService = Depends(get_product_service)):
    try:
        product_by_id = await product_service.get_product(id)
        return product_by_id
    except NotFoundException as e:
        return HTTPException(status_code=404, detail=str(e))

@product_router.put("/{id}", responses={
    200: {"model": ProductResponse},
    404: {"description": "No products found"}
})
async def update_product(id: int, new_product: ProductUpdate, product_service: ProductService = Depends(get_product_service)):
    try:
        updated_product = await product_service.update_product(id, new_product)
        return updated_product
    except NotFoundException as e:
        return HTTPException(status_code=404, detail=str(e))

@product_router.delete("/{id}", responses={
    200: {"model": ProductResponse},
    404: {"description": "No products found"}
})
async def delete_product(id: int, product_service: ProductService = Depends(get_product_service)):
    try:
        deleted_product = await product_service.delete_product(id)
        return deleted_product
    except NotFoundException as e:
        return HTTPException(status_code=404, detail=str(e))

