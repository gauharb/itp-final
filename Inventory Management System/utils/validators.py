import re
import functools


# Regular expressions to verify format

_DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_PRICE_PATTERN = re.compile(r"^\d+(\.\d{1,2})?$")


def is_valid_date(value):
    # Checks the date format YYYY-MM-DD
    return bool(_DATE_PATTERN.match(str(value)))


def is_valid_price(value):
    # Checks that the price is a number with a maximum of 2 decimal places
    return bool(_PRICE_PATTERN.match(str(value)))


def sanitize_name(name):
    # Removes extra spaces from the name
    name = name.strip()
    name = re.sub(r"\s+", " ", name)
    return name


# Decorators

def log_action(func):
    # Decorator: prints the action name to the console
    # Used for tracking inventory operations
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"  [LOG] Executing: {func.__name__}()")
        result = func(*args, **kwargs)
        print(f"  [LOG] Done: {func.__name__}()")
        return result
    return wrapper


def validate_positive(func):
    # Decorator: checks that the second argument of the function is positive.
    # Used for restock and sell.
    @functools.wraps(func)
    def wrapper(self, product_id, amount):
        if amount <= 0:
            raise ValueError(f"Quantity must be positive, received: {amount}")
        return func(self, product_id, amount)
    return wrapper