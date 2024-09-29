import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock
from schemes.product_scheme import ProductCreate
from services.order_service import OrderService, get_order_service
from services.product_service import ProductService, get_product_service
from routers.order_router import order_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.connect import engine, Base
from schemes.order_scheme import OrderCreate,OrderItemCreate

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

    app.include_router(order_router)

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
def mock_order_service():
    return AsyncMock(spec=OrderService)

@pytest.fixture
def mock_product_service():
    return AsyncMock(spec=ProductService)

@pytest.fixture
def client(mock_order_service):
    app = create_app()
    app.dependency_overrides[get_order_service] = lambda: mock_order_service
    app.dependency_overrides[get_product_service] = lambda: mock_product_service
    return TestClient(app)


# Тест для проверки создания заказа
@pytest.mark.asyncio
async def test_create_order_success(client, mock_order_service, mock_product_service):
    order_data = OrderCreate(
        items=[
            OrderItemCreate(product_id=1, quantity=2),
            OrderItemCreate(product_id=2, quantity=3)
        ]
    )
    created_order = {"id": 1, "items": order_data.items, "status": "in_progress"}

    mock_product_service.create_product(product1)
    mock_product_service.create_product(product2)
    mock_order_service.create_order.return_value = created_order

    response = client.post("/orders/", json=order_data.model_dump())

    assert response.status_code == 200
    result = response.json()
    assert result["id"] == 1
    assert result["status"] == "in_progress"
    mock_order_service.create_order.assert_called_once_with(order_data)

# Тест для проверки получения заказа
@pytest.mark.asyncio
async def test_get_order(client, mock_order_service):
    order_id = 1
    order = {"id": order_id, "items": [{"product_id": 1, "quantity": 2}], "status": "created"}

    mock_order_service.get_order.return_value = order

    response = client.get(f"/orders/{order_id}")

    assert response.status_code == 200
    result = response.json()
    assert result["id"] == order_id


