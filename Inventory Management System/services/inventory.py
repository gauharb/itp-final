from models.product import Product, DiscountedProduct
from utils.validators import validate_positive

class ProductNotFoundError(Exception):
    """Error: product not found"""
    pass

class InventoryService:
    """This class stores all items in the dictionary: id -> Product
    The dictionary is chosen because ID search works for O(1) instead of O(n), as in the list."""

    def __init__(self):
        self._products = {}  # id -> Product
        self._categories = set()  # Set of all categories for quick access
        self._next_id = 1  # Auto-incrementing ID for new products

        # Add methods to work with products(add,update,delete, etc.)........

        # Add product

    def add_product(
        self,
        name,
        price,
        quantity,
        category="general",
        description="",
        expiry_date=None,
        discount=None
    ):
        product_id = self._next_id

        if discount is not None:
            product = DiscountedProduct(
                product_id=product_id,
                name=name,
                price=price,
                quantity=quantity,
                category=category,
                description=description,
                expiry_date=expiry_date,
                discount_percent=discount
            )
        else:
            product = Product(
                product_id=product_id,
                name=name,
                price=price,
                quantity=quantity,
                category=category,
                description=description,
                expiry_date=expiry_date
            )

        self._products[product_id] = product
        self._categories.add(category.strip().lower())
        self._next_id += 1

        return product

    # Update product

    def update_product(self, product_id, **fields):
        product = self._get_or_raise(product_id)

        allowed = {
            "name",
            "price",
            "quantity",
            "category",
            "description",
            "expiry_date"
        }

        for field, value in fields.items():
            if field not in allowed:
                raise ValueError(f"Unknown field: {field}")

            setattr(product, field, value)

        if "category" in fields:
            self._categories.add(fields["category"].strip().lower())

        return product
    
    # Delete product

    def remove_product(self, product_id):
        product = self._get_or_raise(product_id)
        del self._products[product_id]
        return product
    
    # Get product by id

    def get_product(self, product_id):
        return self._get_or_raise(product_id)

    # Search and filter

    def search_by_name(self, query):
        """Search products by name"""
        query = query.strip().lower()

        return [
            p for p in self._products.values()
            if query in p.name.lower()
        ]

    def filter_by_category(self, category):
        """Get products from a specific category"""
        cat = category.strip().lower()

        return [
            p for p in self._products.values()
            if p.category == cat
        ]

    def filter_by_price_range(self, min_price, max_price):
        """Get products within a price range"""

        if min_price > max_price:
            raise ValueError("Minimum price cannot be greater than maximum price")

        return [
            p for p in self._products.values()
            if min_price <= p.price <= max_price
        ]

    def get_low_stock(self, threshold=5):
        """Get products with low stock"""

        return [
            p for p in self._products.values()
            if p.is_low_stock(threshold)
        ]

    def get_all_products(self):
        """Get all products sorted by ID"""

        return sorted(
            self._products.values(),
            key=lambda p: p.product_id
        )

    def get_categories(self):
        """Get all categories"""

        return set(self._categories)

    # Inventory management

    @validate_positive
    def restock_product(self, product_id, amount):
        """Increase product quantity"""

        product = self._get_or_raise(product_id)
        product.quantity += amount
        return product
    
    @validate_positive
    def sell(self, product_id, amount):
        ""Sell product ""
        product = self._get_or_raise(product_id)

        if product.quantity < amount:
            raise ValueError(f"Not enough stock: {product.quantity} available")
        
        product.quantity -= amount
        return product
    

    # Expiry Date Features

    def get_expired_products(self):
        """Get all expired products"""

        return [
            p for p in self._products.values()
            if p.is_expired()
        ]

    def get_expiring_soon(self, days=7):
        """
        Get products expiring within the next N days
        Uses filter + lambda
        """

        return list(filter(
            lambda p: p.days_until_expiry() is not None
            and 0 <= p.days_until_expiry() <= days,
            self._products.values()
        ))
    
    
    # Generator

    def iter_products(self):
        """Generator that yields products one-by-one"""

        for product in self._products.values():
            yield product

    # File Loading

    def load_from_list(self, products):
        """Load products list"""

        self._products.clear()
        self._categories.clear()

        for p in products:
            self._products[p.product_id] = p
            self._categories.add(p.category)

        if self._products:
            self._next_id = max(self._products.keys()) + 1
        else:
            self._next_id = 1