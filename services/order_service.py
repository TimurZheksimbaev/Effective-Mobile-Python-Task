from fastapi import Depends
from repositories.order_repository import OrderRepository, get_order_repository
from repositories.product_repository import ProductRepository, get_product_repository
from database.models import Order, OrderItem, OrderStatus
from exceptions import NotEnoughStockException, NotFoundException, InvalidStatusException, NotFoundItemsException
from schemes.order_scheme import OrderCreate

""" Класс сервис для заказов"""
class OrderService:
    def __init__(self, order_repo: OrderRepository, product_repo):
        self.order_repo = order_repo
        self.product_repo = product_repo

    # Создание нового заказа
    async def create_order(self, order_data: OrderCreate):
        order = Order()
        for item in order_data.items:
            product = await self.product_repo.get(item.product_id)
            if product.stock < item.quantity:
                raise NotEnoughStockException(item.product_id, product.stock)
            product.stock -= item.quantity
            order_item = OrderItem(product_id=product.id, quantity=item.quantity)
            order.items.append(order_item)
        return await self.order_repo.create(order)

    # Получение списка заказов
    async def list_orders(self):
        orders = await self.order_repo.list()
        if not orders:
            raise NotFoundItemsException("orders")
        return orders

    # Поолучение заказа поо ID
    async def get_order(self, order_id: int):
        order = await self.order_repo.get(order_id)
        if not order:
            raise NotFoundException("order", order_id)
        return order

    # Редактирование заказа
    async def update_order_status(self, order_id: int, status: str):
        order = await self.get_order(order_id)
        if not order:
            raise NotFoundException("order", order_id)
        if status not in OrderStatus.__members__:
            raise InvalidStatusException(status)
        return await self.order_repo.update_status(order_id, OrderStatus[status])

def get_order_service(
    order_repo: OrderRepository = Depends(get_order_repository),
    product_repo: ProductRepository = Depends(get_product_repository)
):
    return OrderService(order_repo, product_repo)
