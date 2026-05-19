import json
import csv
import os
from models.product import Product, DiscountedProduct


class FileHandler:

    DEFAULT_FILE = os.path.join("data", "inventory.json")


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
    
    def save_json(self, filepath, products):
        os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)
        data = [p.to_dict() for p in products]
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)