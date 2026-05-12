from supabase_client import supabase

def register_user(email, password):
    try:
        if not supabase:
            return {"success": False, "error": "Servicio de base de datos no disponible."}
            
        res = supabase.auth.sign_up({"email": email, "password": password})
        if res.user:
            return {"success": True, "user": res.user}
        return {"success": False, "error": "Error en el registro. Es posible que el usuario ya exista."}
    except Exception as e:
        return {"success": False, "error": str(e)}

def login_user_supabase(email, password):
    try:
        if not supabase:
            return {"success": False, "error": "Servicio de base de datos no disponible."}

        res = supabase.auth.sign_in_with_password({"email": email, "password": password})
        if res.user:
            profile = None
            try:
                profile_res = supabase.table("users").select("*").eq("id", res.user.id).execute()
                profile = profile_res.data[0] if profile_res.data else None
            except:
                profile = None

            return {
                "success": True, 
                "user": res.user, 
                "profile": profile or {
                    "id": res.user.id,
                    "nickname": email.split("@")[0],
                    "role": "user"
                }
            }
        return {"success": False, "error": "Email o contraseña inválidos."}
    except Exception as e:
        return {"success": False, "error": str(e)}
