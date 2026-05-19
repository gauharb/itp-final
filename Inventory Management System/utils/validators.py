import re


# Regular expressions to verify format

_DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_PRICE_PATTERN = re.compile(r"^\d+(\.\d{1,2})?$")


def is_valid_date(value):
    """Checks the date format YYYY-MM-DD"""
    return bool(_DATE_PATTERN.match(str(value)))


def is_valid_price(value):
    """Checks that the price is a number with a maximum of 2 decimal places"""
    return bool(_PRICE_PATTERN.match(str(value)))


def sanitize_name(name):
    """Removes extra spaces from the name"""
    name = name.strip()
    name = re.sub(r"\s+", " ", name)
    return name