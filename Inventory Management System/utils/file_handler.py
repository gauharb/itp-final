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

    def export_csv(self, filepath, products):
        if not products:
            print("  No products to export.")
            return

        os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)

        fields = [
             "id", "name", "category", "price",
             "quantity", "discount_percent",
             "discounted_price", "expiry_date",
             "description"
        ]

        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
            writer.writeheader()

            for p in products:
                row = p.to_dict()
                row["id"] = p.product_id

                if isinstance(p, DiscountedProduct):
                    row["discount_percent"] = p.discount
                    row["discounted_price"] = p.discounted_price()
                else:
                    row["discount_percent"] = ""
                    row["discounted_price"] = ""

                writer.writerow(row)

        print(f"  Export completed → {filepath}")
    def export_low_stock_csv(self, filepath, products, threshold=5):
    
        low = [p for p in products if p.is_low_stock(threshold)]

        if not low:
            print(f"  No products with low stock (threshold={threshold}).")
            return

        self.export_csv(filepath, low)
