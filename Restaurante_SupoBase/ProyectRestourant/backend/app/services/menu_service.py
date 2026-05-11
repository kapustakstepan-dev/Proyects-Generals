class MenuService:
    def __init__(self, supabase_client):
        self.supabase = supabase_client

    def get_active_menu(self):
        res = self.supabase.table("menu").select("*").eq("active", True).execute()
        return res.data

    def get_item_by_id(self, item_id):
        res = self.supabase.table("menu").select("*").eq("id", item_id).execute()
        return res.data[0] if res.data else None

    def add_menu_item(self, data):
        """Admin only logic for adding menu items"""
        res = self.supabase.table("menu").insert(data).execute()
        return res.data[0] if res.data else None
