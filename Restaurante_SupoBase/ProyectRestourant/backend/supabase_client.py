import os
from dotenv import load_dotenv

load_dotenv()

supabase = None

try:
    from supabase import create_client

    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

    if url and key:
        supabase = create_client(url, key)
except Exception as e:
    print("Supabase init error:", str(e))
