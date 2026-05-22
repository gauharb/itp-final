import sys
import os
import unittest
from datetime import date, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from models.product import Product, DiscountedProduct
from services.inventory import InventoryService, ProductNotFoundError

class TestProduct(unittest.TestCase):
    def setUp(self):
        self.product = Product(product_id=1, name="Laptop", price=1200.0, quantity=5)

    def test_basic_attributes(self):
            self.assertEqual(self.product.product_id, 1)
            self.assertEqual(self.product.name, "Laptop")
            self.assertEqual(self.product.price, 1200.0)
            self.assertEqual(self.product.quantity, 5)

    def test_negative_price_raises_error(self):
            with self.assertRaises(ValueError):
                Product(product_id=2, name="X", price=-1.0, quantity=0)

    def test_negative_quantity_raises_error(self):
            with self.assertRaises(ValueError):
                self.product.quantity = -5

    def test_empty_name_raises_error(self):
            with self.assertRaises(ValueError):
                self.product.name = "   "

    def test_is_low_stock_true(self):
            self.assertTrue(self.product.is_low_stock(threshold=5))

    def test_is_low_stock_false(self):
            self.product.quantity = 10
            self.assertFalse(self.product.is_low_stock(threshold=5))

    def test_to_dict_and_from_dict(self):
            d = self.product.to_dict()
            restored = Product.from_dict(d)
            self.assertEqual(restored.product_id, self.product.product_id)
            self.assertEqual(restored.name, self.product.name)
            self.assertEqual(restored.price, self.product.price)

    def test_equality(self):
            p2 = Product(product_id=1, name="Another", price=0, quantity=0)
            self.assertEqual(self.product, p2)

class TestDiscountedProduct(unittest.TestCase):

    def setUp(self):
                    self.dp = DiscountedProduct(
                        product_id=10, name="TV", price=500.0,
                        quantity=3, discount_percent=20.0
                    )

    def test_discounted_price(self):
                    self.assertAlmostEqual(self.dp.discounted_price(), 400.0)

    def test_invalid_discount_raises(self):
                    with self.assertRaises(ValueError):
                        self.dp.discount = 150.0

    def test_to_dict_has_discount(self):
                    d = self.dp.to_dict()
                    self.assertIn("discount_percent", d)

class TestExpiry(unittest.TestCase):

    def test_expired_product(self):
                            yesterday = (date.today() - timedelta(days=1)).isoformat()
                            p = Product(product_id=1, name="Milk", price=1.0, quantity=5, expiry_date=yesterday)
                            self.assertTrue(p.is_expired())

    def test_not_expired_product(self):
                            tomorrow = (date.today() + timedelta(days=1)).isoformat()
                            p = Product(product_id=2, name="Juice", price=2.0, quantity=3, expiry_date=tomorrow)
                            self.assertFalse(p.is_expired())

    def test_no_expiry_date(self):
                            p = Product(product_id=3, name="Salt", price=0.5, quantity=100)
                            self.assertFalse(p.is_expired())

    def test_days_until_expiry(self):
                            future = (date.today() + timedelta(days=10)).isoformat()
                            p = Product(product_id=4, name="Cheese", price=3.0, quantity=2, expiry_date=future)
                            self.assertEqual(p.days_until_expiry(), 10)

    def test_days_until_expiry_none(self):
                            p = Product(product_id=5, name="Water", price=0.5, quantity=50)
                            self.assertIsNone(p.days_until_expiry())

class TestInventoryService(unittest.TestCase):

    def setUp(self):
        self.service = InventoryService()

    def _add_laptop(self):
        return self.service.add_product("Laptop", 1200.0, 5, "electronics")

    def test_add_product(self):
        p = self._add_laptop()
        self.assertIn(p.product_id, self.service)

    def test_id_increments(self):
        p1 = self._add_laptop()
        p2 = self.service.add_product("Mouse", 25.0, 50)
        self.assertEqual(p1.product_id, 1)
        self.assertEqual(p2.product_id, 2)

    def test_get_product_found(self):
        p = self._add_laptop()
        found = self.service.get_product(p.product_id)
        self.assertEqual(found, p)

    def test_get_product_not_found(self):
        with self.assertRaises(ProductNotFoundError):
            self.service.get_product(999)