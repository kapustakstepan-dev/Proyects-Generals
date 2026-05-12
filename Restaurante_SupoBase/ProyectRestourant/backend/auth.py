from backend.supabase_client import supabase

ADMIN_EMAILS = {"admin@gmail.com"}

def register_user(email, password):
    try:
        if not supabase:
            return {"success": False, "error": "Servicio de base de datos no disponible."}
            
        res = supabase.auth.sign_up({"email": email, "password": password})
        if res.user:
            return {"success": True, "user": res.user}
        return {"success": False, "error": "Error en el registro."}
    except Exception as e:
        return {"success": False, "error": str(e)}

def get_user_profile(user):
    if not supabase:
        return None

    try:
        res = supabase.table("users").select("*").eq("id", user.id).execute()
        data = res.data[0] if res.data else None
        
        # Auto-heal: if profile doesn't exist, create it with the correct role
        if not data:
            role = "admin" if user.email in ADMIN_EMAILS else "user"
            new_profile = {
                "id": user.id,
                "nickname": user.email.split("@")[0],
                "role": role
            }
            supabase.table("users").insert(new_profile).execute()
            return new_profile
            
        return data
    except Exception as e:
        print(f"Error en perfil: {e}")
        return None

def login_user_supabase(email, password):
    try:
        if not supabase:
            return {"success": False, "error": "Servicio de base de datos no disponible."}

        res = supabase.auth.sign_in_with_password({"email": email, "password": password})
        if res.user:
            profile = get_user_profile(res.user)
            return {
                "success": True, 
                "user": res.user, 
                "profile": profile
            }
        return {"success": False, "error": "Email o contraseña inválidos."}
    except Exception as e:
        return {"success": False, "error": str(e)}
