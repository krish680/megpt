<<<<<<< HEAD
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

BASE_URL = os.getenv("BASE_URL")

=======
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

BASE_URL = os.getenv("BASE_URL")

>>>>>>> e25fd19efe1b9ce37d47aa9f9c0c7ef17e8eb413
PORT = int(os.getenv("PORT", 10000))