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