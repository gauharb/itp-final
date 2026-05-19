import json
import csv
import os
from models.product import Product, DiscountedProduct


class FileHandler:
    DEFAULT_FILE = os.path.join("data", "inventory.json")