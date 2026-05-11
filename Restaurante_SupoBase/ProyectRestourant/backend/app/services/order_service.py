from datetime import datetime
from ..utils.logging_utils import log_event

class OrderService:
    def __init__(self, supabase_client):
        self.supabase = supabase_client

    def create_order(self, user_id, basket_data):
        """
        Business logic for creating a normalized order.
        1. Validates availability (optional)
        2. Calculates total
        3. Inserts order and items
        """
        try:
            basket_items = []
            total_price = 0
            
            # Data gathering
            for item_id, qty in basket_data.items():
                res = self.supabase.table("menu").select("*").eq("id", int(item_id)).execute()
                if res.data:
                    item = res.data[0]
                    basket_items.append({'item': item, 'quantity': qty})
                    total_price += item['price'] * qty

            if not basket_items:
                return {"success": False, "error": "Empty basket"}

            # Transaction-like insert
            order_res = self.supabase.table("orders").insert({
                "user_id": user_id,
                "total_price": total_price,
                "state": 'confirmed'
            }).execute()

            if not order_res.data:
                return {"success": False, "error": "Order header creation failed"}

            order_id = order_res.data[0]['id']
            items_to_insert = [{
                "order_id": order_id,
                "menu_id": bi['item']['id'],
                "quantity": bi['quantity'],
                "unit_price": bi['item']['price']
            } for bi in basket_items]

            self.supabase.table("order_items").insert(items_to_insert).execute()
            
            log_event("order_created", f"Order {order_id} created", user_id=user_id)
            return {"success": True, "order_id": order_id, "total": total_price}

        except Exception as e:
            log_event("order_error", str(e), user_id=user_id)
            return {"success": False, "error": str(e)}

    def get_user_orders(self, user_id):
        res = self.supabase.table("orders").select("*").eq("user_id", user_id).order("order_time", desc=True).execute()
        return res.data
