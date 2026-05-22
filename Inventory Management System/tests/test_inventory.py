import sys
import os
import unittest
from datetime import date, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from models.product import Product, DiscountedProduct
from services.inventory import InventoryService, ProductNotFoundError