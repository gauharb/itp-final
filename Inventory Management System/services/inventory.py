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
    