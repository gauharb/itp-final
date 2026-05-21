import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from services.inventory import InventoryService, ProductNotFoundError
from services.report import ReportService
from utils.file_handler import FileHandler
from utils.validators import (
    prompt_int,
    prompt_float,
    prompt_nonempty,
    prompt_date,
    confirm,
    format_price,
    format_id,
    log_action
)
DATA_FILE = os.path.join("data", "inventory.json")
EXPORT_CSV = os.path.join("data", "export_full.csv")
LOW_STOCK_CSV = os.path.join("data", "export_low_stock.csv")
EXPIRED_CSV = os.path.join("data", "export_expired.csv")

MENU = """
╔═══════════════════════════════════════╗
║    INVENTORY MANAGEMENT SYSTEM        ║
╠═══════════════════════════════════════╣
║  1.  All products                     ║
║  2.  Add new Product                  ║
║  3.  Remove Product                   ║
║  4.  Update Product                   ║
║  5.  Search by Name                   ║
║  6.  Filter by Category               ║
║  7.  Low Stock                        ║
║  8.  Summary Statistics               ║
║  9.  Restock                          ║
║  10. Sell Product                     ║
║  11. Expiry Report                    ║
║  12. Export to CSV                    ║
║  0.  Save and Exit                    ║
╚═══════════════════════════════════════╝
"""
@log_action
def do_add(service):
    print("\n Add new product ")

    name = prompt_nonempty("Name : ")
    price = prompt_float("Price (EURO €) : ")
    quantity = prompt_int("Quantity : ", min_val=0)
    category = prompt_nonempty("Category : ")
    description = input("Description: ").strip()
    expiry = prompt_date("Expiry Date: ")

    has_discount = confirm("Add discount?")
    discount = None

    if has_discount:
        discount = prompt_float("  Discount (%) : ", min_val=0.0)

    product = service.add_product(
        name=name,
        price=price,
        quantity=quantity,
        category=category,
        description=description,
        expiry_date=expiry,
        discount=discount
    )

    print(
        f"\n  Product added successfully: "
        f"{format_id(product.product_id)} — {product.name}"
    )

    @log_action
    def do_remove(service):
        print("\n Remove Product ")

        pid = prompt_int("  Product ID: ", min_val=1)

        try:
            removed = service.remove_product(pid)

            print(
                f"  Removed: "
                f"{format_id(removed.product_id)} — {removed.name}"
            )

        except ProductNotFoundError as e:
            print(f"  ✗ {e}")

    @log_action
    def do_update(service):
        print("\n Update Product ")

        pid = prompt_int("  Product ID: ", min_val=1)

        try:
            product = service.get_product(pid)

        except ProductNotFoundError as e:
            print(f"  ✗ {e}")
            return

        print(f"  Current product: {product}")

        print("  Available fields: name, price, quantity, category, description, expiry_date")

        field = input("  Which field to update? ").strip().lower()

        if not field:
            print("  Cancelled")
            return

        if field == "price":
            value = prompt_float(f"  New value for '{field}': ")

        elif field == "quantity":
            value = prompt_int(f"  New value for '{field}': ", min_val=0)

        elif field == "expiry_date":
            value = prompt_date("  New expiry date: ")

        else:
            value = prompt_nonempty(f"  New value for '{field}': ")

        try:
            updated = service.update_product(pid, **{field: value})
            print(f"  Updated: {updated}")

        except (ValueError, TypeError) as e:
            print(f"  ✗ {e}")

    def do_search(service):
        query = prompt_nonempty("  Search by name: ")

        results = service.search_by_name(query)

        if not results:
            print("  No products found.")
        else:
            print(f"  Found {len(results)} product(s):")

            for p in results:
                print(
                    f"    {format_id(p.product_id)} "
                    f"{p.name:<25} "
                    f"{format_price(p.price)} "
                    f"quantity={p.quantity}"
                )

    def do_filter_category(service):
        cats = service.get_categories()

        if not cats:
            print("  No categories available.")
            return

        print(f"  Available categories: {', '.join(sorted(cats))}")

        cat = prompt_nonempty("  Category: ")

        results = service.filter_by_category(cat)

        print(f"  Products in '{cat}': {len(results)}")

        for p in results:
            print(
                f"    {format_id(p.product_id)} "
                f"{p.name:<25} "
                f"quantity={p.quantity}"
            )

    @log_action
    def do_restock(service):
        pid = prompt_int("  Product ID   : ", min_val=1)
        amount = prompt_int("  Add Quantity : ", min_val=1)

        try:
            p = service.restock(pid, amount)

            print(
                f"  Restocked {format_id(pid)} — new quantity: {p.quantity}"
            )

        except (ProductNotFoundError, ValueError) as e:
            print(f"  ✗ {e}")

    @log_action
    def do_sell(service):
        pid = prompt_int("  Product ID   : ", min_val=1)
        amount = prompt_int("  Sell Quantity: ", min_val=1)

        try:
            p = service.sell(pid, amount)

            print(
                f"  Sold {amount}× {p.name} — remaining: {p.quantity}"
            )

        except (ProductNotFoundError, ValueError) as e:
            print(f"  ✗ {e}")

    def do_expiry_report(service, report_svc):
        days = prompt_int(
            "  Warn before expiry (days)? [7]: ",
            min_val=1,
            max_val=365
        )

        report_svc.print_expiry_report(
            service.get_all_products(),
            warn_days=days
        )

    def run():
        service = InventoryService()
        file_handler = FileHandler()
        report_svc = ReportService()

        if os.path.exists(DATA_FILE):
            try:
                n = file_handler.load_into_service(service, DATA_FILE)

                print(f"  Loaded {n} product(s) from {DATA_FILE}")

            except (FileNotFoundError, ValueError) as e:
                print(f"  Warning: Failed to load data — {e}")

        else:
            print("  Data file not found. Starting with an empty inventory.")