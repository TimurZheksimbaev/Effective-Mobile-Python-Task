
# Ошибка при отстуствии конкретных данных: товаров или заказов
class NotFoundException(Exception):
    def __init__(self, item: str, id: int):
        super().__init__(
            f"{item} with ID: {id} not found"
        )

# Ошибка при отсутствии данных списком
class NotFoundItemsException(Exception):
    def __init__(self, item: str):
        super().__init__(
            f"No {item} found"
        )

#  Ошибка при отстутствии достаточного количества товара
class NotEnoughStockException(Exception):
    def __init__(self, id: int, amount: int):
        super().__init__(
            f"Not enough products ID: {id} in stock. Available only: {amount} "
        )

# Ошибка при неверном статусе заказа
class InvalidStatusException(Exception):
    def __init__(self, status: str):
        super().__init__(
            f"Invalid status {status}. Available statuses: в процессе, отправлен, доставлен"
        )
