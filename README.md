# Inventory Management System
Final project for Introduction to Programming 2 (Python).

A console app to manage warehouse products and track stock levels.

## Project Description

- Add, update and remove products
- Search by name and filter by category
- Track expiry dates for food products
- Get low stock and out of stock alerts
- Apply discounts to products
- Generate inventory reports by category
- Export data to CSV
- Save and load data from JSON file

## How to run
```bash
python main.py
```
To run tests:

```bash
python -m pytest tests/test_inventory.py -v
```
## Team Members

- Mukhtarova Dana — Report + Validators
- Nurzhan Aisu — File Handler + Main
- Mukazhan Mumina — Tests + Database + README
- Baimagambet Gauhar — Product + Inventory

## Project Structure

main.py                       - main menu and program logic

models/product.py             - Product and DiscountedProduct classes

services/inventory.py         - add, remove, update, search, sell, restock products

services/report.py            - inventory reports and category breakdown

utils/file_handler.py         - load and save JSON, export to CSV

utils/validators.py           - input validation, decorators, regex checks

tests/test_inventory.py       - 36 unit tests

data/inventory.json           - product storage
