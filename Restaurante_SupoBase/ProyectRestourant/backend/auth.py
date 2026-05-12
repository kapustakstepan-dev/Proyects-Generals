from supabase_client import supabase

def register_user(email, password):
    try:
        res = supabase.auth.sign_up({"email": email, "password": password})
        if res.user:
            return {"success": True, "user": res.user}
        return {"success": False, "error": "Sign-up failed. User might already exist."}
    except Exception as e:
        return {"success": False, "error": str(e)}

def login_user_supabase(email, password):
    try:
        res = supabase.auth.sign_in_with_password({"email": email, "password": password})
        if res.user:
            # Fetch profile with fallback to avoid trigger lag issues
            profile = supabase.table("users") \
                .select("*") \
                .eq("id", res.user.id) \
                .execute()

            profile_data = (
                profile.data[0]
                if profile.data
                else {
                    "id": res.user.id,
                    "nickname": email.split("@")[0],
                    "role": "user"
                }
            )
            return {"success": True, "user": res.user, "profile": profile_data}
        return {"success": False, "error": "Invalid email or password."}
    except Exception as e:
        return {"success": False, "error": str(e)}
