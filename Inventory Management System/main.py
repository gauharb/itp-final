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