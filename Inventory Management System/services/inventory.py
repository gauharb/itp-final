from models.product import Product,DiscountedProduct
from utils.validators import validate_positive

class ProductNotFoundError(Exception):
    """Error: product not found"""
    pass

class InventoryService:
    """This class stores all items in the dictionary: id -> Product
    The dictionary is chosen because ID search works for O(1) instead of O(n), as in the list."""


    def __init__(sellf):
        self._products = {}  # id -> Product
        self._categories = set()  # Set of all categories for quick access
        self._next_id = 1  # Auto-incrementing ID for new products

        # Add methods to work with products(add,update,delete, etc.)........


 