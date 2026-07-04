import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

PORT = int(os.getenv("PORT", 10000))
BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:10000")