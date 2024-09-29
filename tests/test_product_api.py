import pytest
from unittest.mock import AsyncMock
from fastapi.testclient import TestClient
from services.product_service import ProductService, get_product_service
from fastapi import FastAPI
from schemes.product_scheme import ProductCreate, ProductResponse, ProductUpdate
from routers.product_router import product_router
from fastapi.middleware.cors import CORSMiddleware
from database.connect import engine
from database.models import Base

def create_app():
    app = FastAPI(
        title="API для управления складом",
        description="Простое API для управления складом. Позволяет добавлять, удалять, обновлять и получать продукты и заказы.",
        version="1.0.0"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(product_router)

    @app.on_event("startup")
    async def startup_event():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    return app

product1 = ProductCreate(
    name="Test 1",
    description="Test Description 1",
    price=123,
    stock=2
)

product2 = ProductCreate(
    name="Test 2",
    description="Test Description 2",
    price=2345,
    stock=4
)

@pytest.fixture
def mock_product_service():
    return AsyncMock(spec=ProductService)


@pytest.fixture
def client(mock_product_service):
    app = create_app()
    app.dependency_overrides[get_product_service] = lambda: mock_product_service
    return TestClient(app)


#  Тестт для создания продутка
@pytest.mark.asyncio
async def test_create_product(client, mock_product_service):
    mock_product_service.create_product.return_value = ProductResponse(id=1, **product1.dict())

    response = client.post("/products/", json=product1.model_dump())

    assert response.status_code == 200
    result = response.json()

    assert result["id"] == 1
    assert result["name"] == "Test 1"


# Тест для получения списка товаров
@pytest.mark.asyncio
async def test_list_products(client, mock_product_service):
    mock_product_service.create_product(product1)

    mock_product_service.create_product(product2)

    products = [
        ProductResponse(
            id=1,
            **product1.dict()
        ),
        ProductResponse(
            id=2,
            **product2.dict()
        )
    ]

    mock_product_service.list_products.return_value = products

    response = client.get("products/")

    assert response.status_code == 200
    result = response.json()

    assert len(result) == 2
    assert result[0]["price"] == 123
    assert result[1]["name"] == "Test 2"

# тест для получния товара по ID
@pytest.mark.asyncio
async def test_get_product_by_id(client, mock_product_service):

    mock_product_service.create_product(product1)

    mock_product_service.get_product.return_value = ProductResponse(id=1, **product1.model_dump())

    response = client.get("/products/1")

    assert response.status_code == 200
    result = response.json()

    assert result["id"] == 1
    assert result["name"] == "Test 1"

# тест для обновления товара
@pytest.mark.asyncio
async def test_update_product(client, mock_product_service):
    update_product1 = ProductUpdate(
        name="Test 3",
    )
    new_product1 = ProductCreate(
        name="Test 3",
        description="Test Description 1",
        price=123,
        stock=2
    )
    mock_product_service.create_product(product1)
    mock_product_service.update_product.return_value = ProductResponse(id=1, **new_product1.model_dump())

    response = client.put("/products/1", json=update_product1.model_dump())

    assert response.status_code == 200
    result = response.json()

    assert result["name"] != product1.name


# тест для удаления товара
@pytest.mark.asyncio
async def test_delete_product_success(client, mock_product_service):
    mock_product_service.create_product(product1)

    mock_product_service.delete_product.return_value = product1

    response = client.delete("/products/1")

    assert response.status_code == 200
    result = response.json()

    assert result == product1.model_dump()
