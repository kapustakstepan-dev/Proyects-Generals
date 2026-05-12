from backend.supabase_client import supabase
from backend.logs import log

def create_order_atomic(user_id, items_to_insert, total_price):
    if not supabase:
        return None
        
    try:
        # 1. Insertar el pedido principal
        order_res = supabase.table("orders").insert({
            "user_id": user_id, 
            "total_price": total_price
        }).execute()
        
        if order_res.data:
            order_id = order_res.data[0]['id']
            
            # 2. Insertar los items del pedido vinculados al order_id
            for i in items_to_insert: 
                i['order_id'] = order_id
                
            supabase.table("order_items").insert(items_to_insert).execute()
            
            log("ORDER_CREATED", {"order_id": order_id, "user_id": user_id})
            return order_id
            
        return None
    except Exception as e:
        log("ORDER_ERROR", str(e))
        return None
