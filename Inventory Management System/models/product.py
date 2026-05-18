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

        # Getters and Setters
    @property
    def product_id(self):
        return self._id

    @property
    def description(self):
        return self._description
    
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value.strip():
            raise ValueError("Name cannot be empty")
        self._name = value.strip()

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("Price cannot be negative")
        self._price = value

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        if value < 0:
            raise ValueError("Quantity cannot be negative")
        self._quantity = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        self._category = value.strip().lower()

    @property
    def expiry_date(self):
        return self._expiry_date

    @expiry_date.setter
    def expiry_date(self, value):
        self._expiry_date = value
