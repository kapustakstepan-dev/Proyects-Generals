from ..utils.logging_utils import log_event
from datetime import datetime

class ReservationService:
    def __init__(self, supabase_client):
        self.supabase = supabase_client

    def create_reservation(self, user_id, dt_str, table_type):
        try:
            time_start = datetime.strptime(dt_str, "%Y-%m-%dT%H:%M")
            if time_start < datetime.now():
                return {"success": False, "error": "Invalid date"}

            res = self.supabase.table("reservations").insert({
                "time_start": time_start.isoformat(),
                "type_table": table_type,
                "user_id": user_id
            }).execute()

            if res.data:
                log_event("reservation_made", f"New reservation for user {user_id}", user_id=user_id)
                return {"success": True, "data": res.data[0]}
            return {"success": False, "error": "Reservation failed"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_user_reservations(self, user_id):
        res = self.supabase.table("reservations").select("*").eq("user_id", user_id).execute()
        return res.data
