from models.product import DiscountedProduct


class ReportService:
    # Class for generating inventory reports

    def summary(self, products):
        # Returns overall inventory statistics
        if not products:
            return {
                "total_products": 0,
                "total_value": 0.0,
                "avg_price": 0.0,
                "categories": set(),
                "low_stock_count": 0,
                "out_of_stock_count": 0,
                "expired_count": 0
            }

        # map + lambda calculating the total inventory value
        total_value = sum(map(lambda p: p.price * p.quantity, products))
        avg_price = sum(map(lambda p: p.price, products)) / len(products)

        # filter products by condition
        low_stock = list(filter(lambda p: p.is_low_stock(5), products))
        out_of_stock = list(filter(lambda p: p.quantity == 0, products))
        expired = list(filter(lambda p: p.is_expired(), products))

        return {
            "total_products": len(products),
            "total_value": round(total_value, 2),
            "avg_price": round(avg_price, 2),
            "categories": {p.category for p in products},
            "low_stock_count": len(low_stock),
            "out_of_stock_count": len(out_of_stock),
            "expired_count": len(expired)
        }

    def category_breakdown(self, products):
        # Returns statistics grouped by category
        breakdown = {}

        for p in products:
            cat = p.category

            if cat not in breakdown:
                breakdown[cat] = {
                    "count": 0,
                    "total_value": 0.0
                }

            breakdown[cat]["count"] += 1
            breakdown[cat]["total_value"] += p.price * p.quantity

        for cat in breakdown:
            breakdown[cat]["total_value"] = round(
                breakdown[cat]["total_value"],
                2
            )

        return breakdown

    def low_stock_items(self, products, threshold=5):
        # Returns products with low stock
        return list(filter(lambda p: p.is_low_stock(threshold), products))

    def out_of_stock_items(self, products):
        # Returns products with zero quantity
        return list(filter(lambda p: p.quantity == 0, products))

    def expired_items(self, products):
        # Returns expired products
        return [p for p in products if p.is_expired()]

    def expiring_soon_items(self, products, warn_days=7):
        # Returns products that will expire soon
        return list(filter(
            lambda p: (
                p.days_until_expiry() is not None
                and 0 <= p.days_until_expiry() <= warn_days
            ),
            products
        ))

    def print_summary(self, products):
        stats = self.summary(products)

        print("\n" + "=" * 50)
        print("   Inventory summary   ")
        print("=" * 50)
        print(f"  Total products      : {stats['total_products']}")
        print(f"  Total value         : ${stats['total_value']:,.2f}")
        print(f"  Average price       : ${stats['avg_price']:,.2f}")
        print(f"  Categories          : {', '.join(sorted(stats['categories'])) or 'none'}")
        print(f"  Low stock           : {stats['low_stock_count']}")
        print(f"  Out of stock        : {stats['out_of_stock_count']}")
        print(f"  Expired             : {stats['expired_count']}")
        print("=" * 50)