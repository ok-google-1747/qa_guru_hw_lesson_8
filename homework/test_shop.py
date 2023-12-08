"""
Протестируйте классы из модуля homework/models.py
"""
import pytest
# from unittest.mock import patch
from homework.models import Product, Cart


@pytest.fixture
def product():
    return Product(
        name="book",
        price=100,
        description="This is a book",
        quantity=1000
    )


@pytest.fixture
def product2():
    return Product(
        name="magazine",
        price=120,
        description="This is a magazine",
        quantity=500
    )


@pytest.fixture
def empty_cart():
    return Cart()


@pytest.fixture
def fill_cart():
    cart = Cart()
    cart.products = {
        Product(
            name="book",
            price=100,
            description="This is a book",
            quantity=1000
        ): 2,
        Product(
            name="magazine",
            price=120,
            description="This is a magazine",
            quantity=500
        ): 3
    }
    return cart


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, product):
        # TODO напишите проверки на метод check_quantity

        result = product.check_quantity(quantity=10)
        assert result is True

        result = product.check_quantity(quantity=1500)
        assert result is False

        # Проверка граничных значений
        result = product.check_quantity(quantity=1000)
        assert result is True

    def test_product_check_quantity_raises(self, product):
        """
        Проверка на исключения
        """
        with pytest.raises(TypeError) as err:
            product.check_quantity(quantity="string parameter")
        assert err.value.args[0] == "В параметре 'quantity' ожидается тип integer"

        with pytest.raises(ValueError) as err:
            product.check_quantity(quantity=-1)
        assert err.value.args[0] == "Параметр 'quantity' должен быть больше нуля"

        # Проверка граничных значений
        with pytest.raises(ValueError) as err:
            product.check_quantity(quantity=0)
        assert err.value.args[0] == "Параметр 'quantity' должен быть больше нуля"

    def test_product_buy(self, product):
        # TODO напишите проверки на метод buy
        result = product.buy(quantity=10)
        assert result is True

        result = product.buy(quantity=1000)
        assert result is True

    def test_product_buy_more_than_available(self, product):
        # TODO напишите проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии
        with pytest.raises(ValueError) as err:
            product.buy(quantity=1200)
        assert err.value.args[0] == f"Товар {product.name} отсутствует на складе в количестве {str(1200)} штук"

    def test_product_buy_raises(self, product):
        """
        Проверка на исключения
        """
        with pytest.raises(TypeError) as err:
            product.buy(quantity="string parameter")
        assert err.value.args[0] == "В параметре 'quantity' ожидается тип integer"

        with pytest.raises(ValueError) as err:
            product.buy(quantity=-1)
        assert err.value.args[0] == "Параметр 'quantity' должен быть больше нуля"

        # Проверка граничных значений
        with pytest.raises(ValueError) as err:
            product.buy(quantity=0)
        assert err.value.args[0] == "Параметр 'quantity' должен быть больше нуля"


class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """

    def test_add_product(self, product, product2, empty_cart):
        empty_cart.add_product(product=product)
        assert empty_cart.products == {product: 1}

        empty_cart.add_product(product=product2)
        assert empty_cart.products == {product: 1, product2: 1}

        empty_cart.add_product(product=product2, buy_count=2)
        assert empty_cart.products == {product: 1, product2: 3}

    def test_remove_product(self, product, product2, fill_cart):
        fill_cart.remove_product(product=product2, remove_count=1)
        assert fill_cart.products == {product: 2, product2: 2}

        fill_cart.remove_product(product=product, remove_count=4)
        assert fill_cart.products == {product2: 2}

        fill_cart.remove_product(product=product2)
        assert fill_cart.products == {}

    def test_remove_product_not_exist(self, product, product2, empty_cart):
        empty_cart.add_product(product=product, buy_count=3)
        assert empty_cart.products == {product: 3}

        with pytest.raises(ValueError) as err:
            empty_cart.remove_product(product=product2)
            assert err.value.args[0] == f"Продукт {product2.name} не добавлен в корзину"

    def test_clear_cart(self, fill_cart):
        fill_cart.clear()
        assert fill_cart.products == {}

    def test_get_total_price(self, fill_cart):
        price = fill_cart.get_total_price()
        assert price == 560

    def test_buy_corrected(self, fill_cart):

        # with patch('homework.models.print') as mock_print:
        #     result = fill_cart.buy()
        #     mock_print.assert_called_once()
        #     mock_print.assert_called_once_with(f"Заказ на сумму {str(560)} оформлен")

        result = fill_cart.buy()
        assert result == f'Заказ на сумму {str(560)} оформлен'

    def test_buy_incorrect(self, product, fill_cart):
        fill_cart.add_product(product=product, buy_count=2000)
        with pytest.raises(ValueError) as err:
            fill_cart.buy()
            assert err.value.args[0] == f"Товар {product.name} отсутствует на складе в количестве {str(2002)} штук"
