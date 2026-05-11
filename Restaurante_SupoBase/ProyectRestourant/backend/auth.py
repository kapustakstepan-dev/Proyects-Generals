from .supabase_client import supabase

def register_user(email, password):
    try:
        res = supabase.auth.sign_up({"email": email, "password": password})
        return {"success": True, "user": res.user} if res.user else {"success": False, "error": "Signup failed"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def login_user_supabase(email, password):
    try:
        res = supabase.auth.sign_in_with_password({"email": email, "password": password})
        if res.user:
            profile = supabase.table("users").select("*").eq("id", res.user.id).execute()
            return {"success": True, "user": res.user, "profile": profile.data[0] if profile.data else None}
        return {"success": False, "error": "Invalid login"}
    except Exception as e:
        return {"success": False, "error": str(e)}
