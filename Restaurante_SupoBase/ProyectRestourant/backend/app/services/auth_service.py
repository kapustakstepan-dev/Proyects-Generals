from ..utils.logging_utils import log_event

class AuthService:
    def __init__(self, supabase_client):
        self.supabase = supabase_client

    def register(self, email, password):
        try:
            res = self.supabase.auth.sign_up({"email": email, "password": password})
            if res.user:
                log_event("user_registered", f"New user signed up: {email}")
                return {"success": True, "user": res.user}
            return {"success": False, "error": "Sign up failed"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def login(self, email, password):
        try:
            res = self.supabase.auth.sign_in_with_password({"email": email, "password": password})
            if res.user:
                profile = self.supabase.table("users").select("*").eq("id", res.user.id).execute()
                log_event("user_logged_in", f"User logged in: {email}", user_id=res.user.id)
                return {"success": True, "user": res.user, "profile": profile.data[0] if profile.data else None}
            return {"success": False, "error": "Invalid credentials"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_profile(self, user_id):
        res = self.supabase.table("users").select("*").eq("id", user_id).execute()
        return res.data[0] if res.data else None
