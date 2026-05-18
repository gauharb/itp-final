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

    def is_low_stock(self, threshold=5):
        """Returns True if product is not enough"""
        return self._quantity <= threshold

    def is_expired(self):
        """Returns True if the expiration date has passed"""
        if self._expiry_date is None:
            return False
        expiry = date.fromisoformat(self._expiry_date)
        return expiry < date.today()

    def days_until_expiry(self):
        """Returns the number of days before the deadline expires.None if no date"""
        if self._expiry_date is None:
            return None
        expiry = date.fromisoformat(self._expiry_date)
        delta = expiry - date.today()
        return delta.days
    
    def to_dict(self):
        """Converts an object into a dictionary (to save as JSON)"""
        return {
            "id": self._id,
            "name": self._name,
            "price": self._price,
            "quantity": self._quantity,
            "category": self._category,
            "description": self._description,
            "expiry_date": self._expiry_date
        }

    @classmethod
    def from_dict(cls, data):
        """Creates a Product object from the dictionary (when loaded from JSON)"""
        return cls(
            product_id=int(data["id"]),
            name=str(data["name"]),
            price=float(data["price"]),
            quantity=int(data["quantity"]),
            category=data.get("category", "general"),
            description=data.get("description", ""),
            expiry_date=data.get("expiry_date", None)
        )