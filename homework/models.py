from dataclasses import dataclass


@dataclass
class Product:
    """
    Класс продукта
    """
    name: str
    price: float
    description: str
    quantity: int

    # def __init__(self, name, price, description, quantity):
    #     self.name = name
    #     self.price = price
    #     self.description = description
    #     self.quantity = quantity

    # def __eq__(self, other) -> bool:
    #     return (self.name == other.name and
    #     self.price == other.price and
    #     self.quantity == other.quantity and
    #     self.description == other.description)

    def check_quantity(self, quantity) -> bool:
        """
        TODO Верните True если количество продукта больше или равно запрашиваемому
            и False в обратном случае
        """
        if isinstance(quantity, int) is False:
            raise TypeError("В параметре 'quantity' ожидается тип integer")
        elif quantity <= 0:
            raise ValueError("Параметр 'quantity' должен быть больше нуля")

        if self.quantity >= quantity:
            return True
        return False

    def buy(self, quantity):
        """
        TODO реализуйте метод покупки
            Проверьте количество продукта используя метод check_quantity
            Если продуктов не хватает, то выбросите исключение ValueError
        """
        if isinstance(quantity, int) is False:
            raise TypeError("В параметре 'quantity' ожидается тип integer")
        elif quantity <= 0:
            raise ValueError("Параметр 'quantity' должен быть больше нуля")

        if self.check_quantity(quantity) is False:
            raise ValueError(f"Товар {self.name} отсутствует на складе в количестве {quantity} штук")
        return True

    def __hash__(self):
        return hash(self.name + self.description)


@dataclass
class Cart:
    """
    Класс корзины. В нем хранятся продукты, которые пользователь хочет купить.
    TODO реализуйте все методы класса
    """

    # Словарь продуктов и их количество в корзине
    products: dict[Product, int]

    def __init__(self):
        # По-умолчанию корзина пустая
        self.products = {}

    def add_product(self, product: Product, buy_count=1):
        """
        Метод добавления продукта в корзину.
        Если продукт уже есть в корзине, то увеличиваем количество
        """

        for added_product in self.products.keys():
            if product.__eq__(added_product) is True:
                self.products[product] += buy_count
                return

        self.products[product] = buy_count
        return

    def remove_product(self, product: Product, remove_count=None):
        """
        Метод удаления продукта из корзины.
        Если remove_count не передан, то удаляется вся позиция
        Если remove_count больше, чем количество продуктов в позиции, то удаляется вся позиция
        """
        for added_product in self.products.keys():
            if product.__eq__(added_product) is True:
                if remove_count is None or remove_count >= self.products[added_product]:
                    self.products.pop(added_product)
                    return
                else:
                    self.products[added_product] -= remove_count
                    return
        raise ValueError(f"Продукт {product.name} не добавлен в корзину")

    def clear(self):
        return self.products.clear()

    def get_total_price(self) -> float:
        total_price = 0
        for added_product in self.products.keys():
            total_price += self.products[added_product] * added_product.price
        return total_price

    def buy(self):
        """
        Метод покупки.
        Учтите, что товаров может не хватать на складе.
        В этом случае нужно выбросить исключение ValueError
        """

        for added_product in self.products.keys():
            added_product.buy(quantity=self.products[added_product])
        total_price = self.get_total_price()
        print(f'Заказ на сумму {total_price} оформлен')
        return f'Заказ на сумму {total_price} оформлен'
