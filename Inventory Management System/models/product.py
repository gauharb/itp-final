from datetime import date


class Product:
    def __init__(self, product_id, name, price, quantity, category="general", description="", expiry_date=None):
        # Validation on creation
        if price < 0:
            raise ValueError("Price cannot be negative")
        if quantity < 0:
            raise ValueError("Quantity cannot be negative")

        self._id = product_id
        self._name = name.strip()
        self._price = price
        self._quantity = quantity
        self._category = category.strip().lower()
        self._description = description
        self._expiry_date = expiry_date  # format "YYYY-MM-DD" or None