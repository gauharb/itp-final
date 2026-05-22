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