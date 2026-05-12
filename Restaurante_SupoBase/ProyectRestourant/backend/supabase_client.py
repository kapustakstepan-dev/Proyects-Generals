import os
import sys
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("\n[ERROR] Missing SUPABASE_URL or SUPABASE_KEY in environment variables.")
    print("Please check your .env file or Vercel dashboard.")
    sys.exit(1)

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print(f"[SUCCESS] Connected to Supabase: {SUPABASE_URL}")
except Exception as e:
    print(f"[FATAL] Could not initialize Supabase client: {e}")
    sys.exit(1)
