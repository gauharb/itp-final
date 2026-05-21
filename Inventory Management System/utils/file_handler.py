import json
import csv
import os
from models.product import Product, DiscountedProduct


class FileHandler:

    DEFAULT_FILE = os.path.join("data", "inventory.json")

    # JSON

    def load_json(self, filepath):
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")

        with open(filepath, "r", encoding="utf-8") as f:
            try:
                raw = json.load(f)
            except json.JSONDecodeError as e:
                raise ValueError(f"Error in JSON file: {e}")

        products = []
        for item in raw:
            if "discount_percent" in item:
                products.append(DiscountedProduct.from_dict(item))
            else:
                products.append(Product.from_dict(item))

        return products