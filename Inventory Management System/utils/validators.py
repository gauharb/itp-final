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


# Functions for user input

def prompt_int(prompt, min_val=0, max_val=100000):
    # Prompts the user to enter an integer within a range
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
            if min_val <= value <= max_val:
                return value
            else:
                print(f"  Please enter a number between {min_val} and {max_val}.")
        except ValueError:
            print("  That's not a valid number. Please try again.")


def prompt_float(prompt, min_val=0.0):
    # Prompts the user to enter a float
    while True:
        raw = input(prompt).strip()
        if not is_valid_price(raw):
            print("  Please enter a valid price (e.g., 9.99)")
            continue

        value = float(raw)
        if value >= min_val:
            return value

        print(f"  Value must be >= {min_val}.")


def prompt_nonempty(prompt):
    # Prompts the user to enter a non-empty string
    while True:
        value = input(prompt).strip()
        if value:
            return sanitize_name(value)

        print("  Field cannot be empty.")


def prompt_date(prompt):
    # Prompts the user to enter a date in YYYY-MM-DD format. Can be skipped.
    while True:
        value = input(prompt + " (YYYY-MM-DD or Enter to skip): ").strip()

        if value == "":
            return None

        if is_valid_date(value):
            return value

        print("  Invalid format. Please use YYYY-MM-DD (e.g., 2026-12-31)")


def confirm(prompt):
    # Prompts the user to confirm an action
    answer = input(f"{prompt} [y/n]: ").strip().lower()
    return answer in ("y", "yes")


# Formatting helpers

format_price = lambda amount: f"${amount:,.2f}"
format_id = lambda pid: f"#{pid:04d}"